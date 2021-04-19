from django.core.exceptions import ValidationError

def validate_numeric(value):
    if not value.isnumeric():
        raise ValidationError("Ce champ doit être numérique")