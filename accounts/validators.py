from django.core.exceptions import ValidationError


def validate_file_size(value):

    max_size = 5 * 1024 * 1024   # 5 MB

    if value.size > max_size:

        raise ValidationError(
            "Maximum file size is 5 MB."
        )




def validate_image_extension(value):

    allowed_extensions = [
        "jpg",
        "jpeg",
        "png",
    ]

    extension = value.name.split(".")[-1].lower()

    if extension not in allowed_extensions:

        raise ValidationError(
            "Only JPG, JPEG and PNG files are allowed."
        )