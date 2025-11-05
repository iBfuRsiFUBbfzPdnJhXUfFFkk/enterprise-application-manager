from datetime import datetime
from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from gitlab import Gitlab
from gitlab.v4.objects import GroupMember

from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import (
    convert_and_enforce_utc_timezone,
)
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from git_lab.apis.common.get_common_query_parameters import (
    GitLabApiCommonQueryParameters,
    get_common_query_parameters,
)
from gitlab_sync.models import GitLabSyncGroup, GitLabSyncJobTracker, GitLabSyncUser
from gitlab_sync.utilities import (
    SyncResult,
    check_job_cancelled,
    handle_gitlab_api_errors,
    run_sync_in_background,
)


def _sync_users_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync users with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncUser", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting users sync...")

    query_parameters: GitLabApiCommonQueryParameters = get_common_query_parameters(
        request=request
    )

    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        sync_result.add_log("❌ Failed to get GitLab client")
        sync_result.add_failure("Failed to get GitLab client")
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    git_lab_groups: QuerySet[GitLabSyncGroup] = cast_query_set(
        typ=GitLabSyncGroup,
        val=GitLabSyncGroup.objects.all(),
    )

    if not git_lab_groups.exists():
        sync_result.add_log(
            "❌ No groups found - please sync groups first using the 'Sync Groups' button"
        )
        sync_result.add_failure(
            "No groups found - please sync groups first using the 'Sync Groups' button"
        )
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    group_count = git_lab_groups.count()
    sync_result.add_log(
        f"Syncing users from {group_count} groups incrementally..."
    )

    processed_count = 0
    estimated_total = group_count * 10  # Rough estimate
    seen_user_ids = set()  # Track users we've already processed to avoid duplicates

    for group_idx, git_lab_group in enumerate(git_lab_groups, 1):
        # Check if job was cancelled
        if check_job_cancelled(sync_result.job_tracker_id):
            sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
            sync_result.finish()
            print(f"[GitLabSync] {sync_result}")
            return

        sync_result.add_log(
            f"📥 About to fetch users from group {git_lab_group.full_path} (group {group_idx}/{group_count})..."
        )

        members, error = handle_gitlab_api_errors(
            func=lambda: cast(
                list[GroupMember],
                git_lab_client.groups.get(id=git_lab_group.id).members.list(
                    **query_parameters
                ),
            ),
            entity_name=f"Members for group {git_lab_group.full_path}",
            max_retries=3,
        )

        if error:
            sync_result.add_log(
                f"❌ Error fetching members for {git_lab_group.full_path}: {error}"
            )
            sync_result.add_failure(error)
            continue

        if not members:
            sync_result.add_log(f"⊘ No members found in group {git_lab_group.full_path}")
            continue

        sync_result.add_log(
            f"✓ Fetched {len(members)} members from {git_lab_group.full_path}, about to process..."
        )

        # Process each member immediately
        for member in members:
            # Check if job was cancelled
            if check_job_cancelled(sync_result.job_tracker_id):
                sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
                sync_result.finish()
                print(f"[GitLabSync] {sync_result}")
                return

            processed_count += 1
            member_dict = member.asdict()
            user_id: int | None = member_dict.get("id")

            if user_id is None:
                sync_result.add_skip()
                continue

            # Skip if we've already processed this user from another group
            if user_id in seen_user_ids:
                sync_result.add_skip()
                sync_result.update_progress(
                    processed_count,
                    estimated_total,
                    f"⊘ Skipped already-processed user {member_dict.get('username')}",
                )
                continue

            seen_user_ids.add(user_id)

            try:
                sync_result.add_log(f"💾 About to get_or_create user {user_id} in database...")
                git_lab_user, created = GitLabSyncUser.objects.get_or_create(
                    id=user_id
                )
                sync_result.add_log(
                    f"✓ Database get_or_create succeeded for user {user_id} (created={created})"
                )

                # Check if we need to update (compare created_at from GitLab with our last_synced_at)
                user_created_at = convert_and_enforce_utc_timezone(
                    datetime_string=member_dict.get("created_at")
                )

                needs_update = created or (
                    git_lab_user.last_synced_at is None
                    or (
                        user_created_at
                        and user_created_at > git_lab_user.last_synced_at
                    )
                )

                if not needs_update:
                    sync_result.add_skip()
                    sync_result.update_progress(
                        processed_count,
                        estimated_total,
                        f"⊘ Skipped unchanged user {member_dict.get('username')}",
                    )
                    continue

                # Update user fields
                git_lab_user.name = member_dict.get("name")
                git_lab_user.username = member_dict.get("username")
                git_lab_user.email = member_dict.get("email")
                git_lab_user.state = member_dict.get("state")
                git_lab_user.avatar_url = member_dict.get("avatar_url")
                git_lab_user.web_url = member_dict.get("web_url")
                git_lab_user.locked = member_dict.get("locked", False)
                git_lab_user.bot = member_dict.get("bot", False)

                git_lab_user.created_at = user_created_at
                git_lab_user.expires_at = convert_and_enforce_utc_timezone(
                    datetime_string=member_dict.get("expires_at")
                )
                git_lab_user.last_synced_at = datetime.now()

                sync_result.add_log(f"💾 About to save user {user_id} to database...")
                git_lab_user.save()
                sync_result.add_log(f"✓ Database save succeeded for user {user_id}")
                sync_result.add_success()
                sync_result.update_progress(
                    processed_count,
                    estimated_total,
                    f"✓ Synced user {git_lab_user.username}",
                )

            except Exception as error:
                import traceback

                error_trace = traceback.format_exc()
                error_msg = f"Failed to save user {user_id}: {str(error)}"
                sync_result.add_failure(error_msg)
                sync_result.add_log(f"❌ {error_msg}")
                print(f"[GitLabSync] {error_msg}")
                print(f"[GitLabSync] Stack trace:\n{error_trace}")
                continue

        # Update estimate based on actual users found
        estimated_total = max(
            estimated_total, processed_count + (group_count - group_idx) * 10
        )

    sync_result.add_log(
        f"✓ Sync complete: {sync_result.synced_count} synced, "
        f"{sync_result.skipped_count} skipped, {sync_result.failed_count} failed"
    )
    sync_result.finish()
    print(f"[GitLabSync] {sync_result}")


def gitlab_sync_users_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync GitLab users from GitLab EE 17.11.6 with background job tracking.

    This API endpoint fetches users from all GitLab groups and syncs them
    to the local database with enhanced error handling and retry logic.

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background("users", _sync_users_background, request)

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "users"}
    )
