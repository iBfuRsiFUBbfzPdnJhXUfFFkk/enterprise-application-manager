from core.models.this_server_configuration import ThisServerConfiguration


def get_gitlab_hostname() -> str | None:
    this_server_configuration: ThisServerConfiguration | None = ThisServerConfiguration.objects.last()
    if this_server_configuration is None:
        return None
    return this_server_configuration.connection_gitlab_hostname
