from gitlab.base import RESTObject


def calculate_delivered_issues(
        all_group_issues: list[RESTObject] | None = None,
) -> tuple[dict, dict] | None:
    delivered_issues = {}
    project_mapping = {}  # Store project IDs per developer

    for issue in all_group_issues:
        if issue.state == "closed":  # Only consider closed issues as delivered
            weight = issue.weight or 0 # Default weight to 0 if not set
            project_id = issue.project_id
            assignees = issue.assignees or []

            for assignee in assignees:
                gitlab_username = assignee["username"]

                # Initialize if not already present
                if gitlab_username not in delivered_issues:
                    delivered_issues[gitlab_username] = {"count": 0, "weight": 0}
                    project_mapping[gitlab_username] = set()  # Use a set for unique projects

                # Track issue count and weight
                delivered_issues[gitlab_username]["count"] += 1
                delivered_issues[gitlab_username]["weight"] += weight

                # Add project ID to track context switching
                if project_id:
                    project_mapping[gitlab_username].add(project_id)

    return delivered_issues, project_mapping
