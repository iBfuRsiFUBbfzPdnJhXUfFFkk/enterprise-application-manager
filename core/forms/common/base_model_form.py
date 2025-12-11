from django.forms import ModelForm, TextInput, Textarea, Select, SelectMultiple, CheckboxInput, NumberInput, EmailInput, URLInput, DateInput, DateTimeInput, TimeInput, FileInput


class BaseModelForm(ModelForm):
    """
    Base model form that automatically adds Tailwind CSS classes to all form widgets.

    This ensures consistent styling across all forms without having to manually add
    CSS classes to each widget definition.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define Tailwind CSS classes for different widget types
        text_input_classes = "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        textarea_classes = "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        select_classes = "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        checkbox_classes = "h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
        file_input_classes = "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"

        # Apply classes to all form fields
        for field_name, field in self.fields.items():
            widget = field.widget
            existing_classes = widget.attrs.get('class', '')

            # Skip if widget already has custom classes (don't override)
            if existing_classes:
                continue

            # Apply appropriate classes based on widget type
            if isinstance(widget, (TextInput, NumberInput, EmailInput, URLInput, DateInput, DateTimeInput, TimeInput)):
                widget.attrs['class'] = text_input_classes
            elif isinstance(widget, Textarea):
                widget.attrs['class'] = textarea_classes
            elif isinstance(widget, (Select, SelectMultiple)):
                widget.attrs['class'] = select_classes
            elif isinstance(widget, CheckboxInput):
                widget.attrs['class'] = checkbox_classes
            elif isinstance(widget, FileInput):
                widget.attrs['class'] = file_input_classes
