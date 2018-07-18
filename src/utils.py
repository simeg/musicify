ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file_type(filename: str) -> bool:
    if filename == 'blob':
        return True
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def exists(value) -> bool:
    if value is None:
        return False
    return True
