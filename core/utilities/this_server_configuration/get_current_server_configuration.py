from core.models.this_server_configuration import ThisServerConfiguration


def get_current_server_configuration() -> ThisServerConfiguration | None:
    return ThisServerConfiguration.objects.last()
