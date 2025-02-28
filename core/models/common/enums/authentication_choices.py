AUTHENTICATION_TYPE_AD: str = "Active Directory (AD)"
AUTHENTICATION_TYPE_CUSTOM: str = "Custom"

AUTHENTICATION_TYPE_CHOICES: list[tuple[str, str]] = [
    (AUTHENTICATION_TYPE_AD, AUTHENTICATION_TYPE_AD),
    (AUTHENTICATION_TYPE_CUSTOM, AUTHENTICATION_TYPE_CUSTOM),
]
