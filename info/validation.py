from rest_framework.validators import ValidationError

def validate_company_phone_number(value):
    """
    Validates that the company phone number consists only of digits 
    and is exactly 8 characters long.
    """
    if not value.isdigit():
        raise ValidationError('Company phone number must contain only English digits.')
    
    if len(value) != 8:
        raise ValidationError('Home phone number must be exactly 8 digits long.')
    
    return value


def validate_version_format(value):
    """
    Version format validation:
    The version must start with the letter 'v' and
    consist of three numeric parts separated by periods, e.g. v1.0.0
    """
    if not value.lower().startswith('v'):
        raise ValidationError("Version must start with the letter 'v'.")
    
    parts = value[1:].split('.')
    if len(parts) != 3:
        raise ValidationError("Version must be in the format v1.0.0.")
    
    for part in parts:
        if not part.isdigit():
            raise ValidationError("Each part of the version must be a number.")
