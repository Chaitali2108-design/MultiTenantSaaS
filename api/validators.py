from django.core.exceptions import ValidationError


ALLOWED_IMAGE_TYPES = [
    "image/jpeg",
    "image/png",
    "image/webp",
]


MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB



def validate_image_file(file):

    # Check file size

    if file.size > MAX_FILE_SIZE:

        raise ValidationError(
            "Image size cannot exceed 2MB"
        )


    # Check content type

    if file.content_type not in ALLOWED_IMAGE_TYPES:

        raise ValidationError(
            "Only JPG, PNG and WEBP images are allowed"
        )


    return file