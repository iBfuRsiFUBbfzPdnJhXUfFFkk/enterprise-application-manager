import logging

from django.db.models import Model
from django.forms import ModelForm

logger = logging.getLogger(__name__)


def generic_encrypted_save(
        model_form: ModelForm,
        instance: Model,
        data_points: list[str] | None = None,
) -> Model:
    """
    Save encrypted fields for a model instance, preserving existing values when form fields are blank.

    This function handles the critical case where a user edits a record but leaves encrypted
    fields blank - in such cases, the existing encrypted value should be preserved rather than
    overwritten with an empty/None value.

    Args:
        model_form: The ModelForm containing cleaned data
        instance: The model instance to save
        data_points: List of encrypted field names (e.g., ['encrypted_password'])

    Returns:
        The saved model instance
    """
    if data_points is None:
        return instance

    for data_point in data_points:
        encrypted_value: str | None = model_form.cleaned_data[data_point]

        # CRITICAL FIX: Check if value is blank/empty
        if not encrypted_value or (isinstance(encrypted_value, str) and encrypted_value.strip() == ""):
            # Check if instance already has encrypted data in this field
            existing_encrypted = getattr(instance, data_point, None)

            if existing_encrypted:
                # PRESERVE existing encrypted value - don't overwrite with empty value
                logger.info(
                    f"Preserving existing encrypted value for {instance.__class__.__name__}.{data_point} "
                    f"(id={instance.pk}) - form field was blank"
                )
                continue  # Skip this field, keep existing value
            else:
                # No existing value - it's intentionally empty, save None
                logger.debug(
                    f"Saving None for {instance.__class__.__name__}.{data_point} "
                    f"(id={instance.pk}) - field is intentionally empty"
                )
                # Continue to setter below with None/empty value

        else:
            # Value has content - encrypt and save the new value
            logger.info(
                f"Updating encrypted value for {instance.__class__.__name__}.{data_point} "
                f"(id={instance.pk}) - new value provided"
            )

        # Call the setter method to encrypt and save
        getattr(instance, f"set_{data_point}")(encrypted_value)

    instance.save()
    return instance
