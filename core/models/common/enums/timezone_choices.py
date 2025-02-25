TIMEZONES: dict[str, str] = {
    "AKST": "Alaska Standard Time (AKST)",
    "AST": "Atlantic Standard Time (AST)",
    "CST": "Central Standard Time (CST)",
    "EST": "Eastern Standard Time (EST)",
    "HST": "Hawaii-Aleutian Standard Time (HST)",
    "MST": "Mountain Standard Time (MST)",
    "PST": "Pacific Standard Time (PST)",
}

TIMEZONE_CHOICES: list[tuple[str, str]] = [(code, name) for code, name in TIMEZONES.items()]