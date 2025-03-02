from core.settings.common.environment import env

DEBUG: bool = env.bool(default=False, var='DEBUG')
