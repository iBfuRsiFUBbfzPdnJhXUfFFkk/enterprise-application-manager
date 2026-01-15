from django.forms import ModelForm


class BaseModelForm(ModelForm):
    """
    Base model form for consistent form behavior across the application.

    Form styling is handled by global CSS (static/css/styles.css) which
    applies styles to all form elements without needing explicit CSS classes.

    Note: Forms inherit visible borders and proper styling from the global
    CSS file to ensure Django form fields are properly displayed.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # No automatic class application needed - styling handled by global CSS
