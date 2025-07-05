from django.core.exceptions import ValidationError
import os

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # Get the file extension
    valid_extensions = [
        '.jpg', '.jpeg', '.png', '.heic', 
        '.mp4', '.mp3', '.pdf', '.mov', '.odf'
    ]
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            f'Unsupported file extension. Allowed extensions: {", ".join(valid_extensions)}'
        )