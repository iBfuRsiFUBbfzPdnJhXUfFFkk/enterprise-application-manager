import time
from typing import Any, Callable, TypeVar

from gitlab.exceptions import (
    GitlabAuthenticationError,
    GitlabError,
    GitlabGetError,
    GitlabListError,
)

T = TypeVar("T")


def handle_gitlab_api_errors(
    func: Callable[[], T],
    entity_name: str,
    max_retries: int = 3,
    backoff_factor: float = 2.0,
) -> tuple[T | None, str | None]:
    """
    Execute a GitLab API function with error handling and retry logic.

    Args:
        func: Function to execute that makes GitLab API calls
        entity_name: Name of the entity being synced (for logging)
        max_retries: Maximum number of retry attempts (default: 3)
        backoff_factor: Exponential backoff multiplier (default: 2.0)

    Returns:
        Tuple of (result, error_message)
        - result: Function return value on success, None on failure
        - error_message: Error description on failure, None on success

    Example:
        result, error = handle_gitlab_api_errors(
            func=lambda: project.issues.list(),
            entity_name="Project Issues",
            max_retries=3
        )
        if error:
            print(f"Failed to sync: {error}")
        else:
            process_issues(result)
    """
    last_error = None

    for attempt in range(max_retries):
        try:
            result = func()
            return result, None

        except GitlabAuthenticationError as error:
            error_msg = (
                f"Authentication failed for {entity_name}: {error.error_message}"
            )
            print(f"[GitLabSync] {error_msg}")
            return None, error_msg

        except GitlabGetError as error:
            # Check for 403 Forbidden - don't retry, return immediately
            if hasattr(error, "response_code") and error.response_code == 403:
                error_msg = f"403 Forbidden: Access denied to {entity_name}"
                print(f"[GitLabSync] {error_msg}")
                return None, error_msg

            error_msg = f"Failed to get {entity_name}: {error.error_message}"
            print(f"[GitLabSync] {error_msg}")
            last_error = error_msg

            if attempt < max_retries - 1:
                sleep_time = backoff_factor**attempt
                print(
                    f"[GitLabSync] Retrying in {sleep_time}s "
                    f"(attempt {attempt + 1}/{max_retries})..."
                )
                time.sleep(sleep_time)
            continue

        except GitlabListError as error:
            # Check for 403 Forbidden - don't retry, return immediately
            if hasattr(error, "response_code") and error.response_code == 403:
                error_msg = f"403 Forbidden: Access denied to {entity_name}"
                print(f"[GitLabSync] {error_msg}")
                return None, error_msg

            error_msg = f"Failed to list {entity_name}: {error.error_message}"
            print(f"[GitLabSync] {error_msg}")
            last_error = error_msg

            if attempt < max_retries - 1:
                sleep_time = backoff_factor**attempt
                print(
                    f"[GitLabSync] Retrying in {sleep_time}s "
                    f"(attempt {attempt + 1}/{max_retries})..."
                )
                time.sleep(sleep_time)
            continue

        except GitlabError as error:
            error_msg = f"GitLab API error for {entity_name}: {str(error)}"
            print(f"[GitLabSync] {error_msg}")
            last_error = error_msg

            if attempt < max_retries - 1:
                sleep_time = backoff_factor**attempt
                print(
                    f"[GitLabSync] Retrying in {sleep_time}s "
                    f"(attempt {attempt + 1}/{max_retries})..."
                )
                time.sleep(sleep_time)
            continue

        except Exception as error:
            import traceback
            error_trace = traceback.format_exc()
            error_msg = f"Unexpected error for {entity_name}: {str(error)}"
            print(f"[GitLabSync] {error_msg}")
            print(f"[GitLabSync] Stack trace:\n{error_trace}")
            return None, error_msg

    return None, last_error
