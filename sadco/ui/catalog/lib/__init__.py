from io import BytesIO
from flask import Response, send_file
import zipfile


def download_zipped_file(file_name, data) -> Response:
    """
    Check if the data is already zipped. If it isn't, zip before sending.
    """
    if zipfile.is_zipfile(BytesIO(data)):
        zip_buffer = BytesIO(data)
    else:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, mode='w') as zip_file:
            zip_file.writestr(file_name, data)
        zip_buffer.seek(0)

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=file_name
    )
