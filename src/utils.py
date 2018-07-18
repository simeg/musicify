ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_FILE_NAME = {'blob'}

def allowed_file_type(filename: str) -> bool:
    if filename in ALLOWED_FILE_NAME:
        return True
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def exists(value) -> bool:
    if value is None:
        return False
    return True
