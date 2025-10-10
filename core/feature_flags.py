"""
Feature Flags Configuration

This module contains boolean feature flags that control the availability of
features throughout the Enterprise Application Manager application.

Feature flags allow features to be turned on/off without code changes,
making it easier to:
- Roll out features gradually
- Test features in production with limited users
- Quickly disable problematic features
- Manage features across different environments
"""

# Authentication Features
FEATURE_REMEMBER_ME_LOGIN = True
"""
Enable "Remember Me" functionality on the login page.
When enabled, users can choose to save their username and extend their session.
Default: True
"""

# Future feature flags can be added below
# Example:
# FEATURE_TWO_FACTOR_AUTH = False
# FEATURE_DARK_MODE = True
# FEATURE_BETA_DASHBOARD = False
