from django.utils.text import slugify

from .models import UploadedFile


class FileUploadException(Exception):
    pass


def unique_filename(name):
    parts = name.split(".")
    name = ".".join(parts[0:-1])
    suffix = parts[-1]
    name = slugify(name)

    full_name = f"{name}.{suffix}"
    i = 0

    while UploadedFile.objects.filter(file_name=full_name).exists():
        i += 1
        full_name = f"{name}{i}.{suffix}"

    return full_name


def handle_uploaded_file(file, type):
    if type not in ["image", "audio"]:
        raise FileUploadException("Unknown type. Accepted values: image, audio")

    if type == "image" and not file.content_type.startswith("image/"):
        raise FileUploadException("The file must be an image.")
    if type == "audio" and not file.content_type.startswith("audio/"):
        raise FileUploadException("The file must be an audio file.")

    name = unique_filename(file.name)
    file.name = name
    instance = UploadedFile(
        file=file,
        file_name=name,
        file_type=type,
        # TODO created_by=user
    )
    instance.save()
    return {"name": name, "file": instance.file}
