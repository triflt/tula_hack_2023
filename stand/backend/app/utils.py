import contextlib
import json
import os
import uuid

import jsonschema
from pathlib import Path
from typing import Callable

from flask import abort, request
from werkzeug.utils import secure_filename

BASE_SCHEMA_PATH = Path('stand/backend/app/schemas')
TMP_UPLOAD_FOLDER = Path('stand/backend/app/tmp/file_uploads')


def validate_json(schema_filename: str):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            with open(BASE_SCHEMA_PATH / schema_filename) as fd:
                try:
                    jsonschema.validate(request.json, json.load(fd))
                except jsonschema.ValidationError as e:
                    abort(400, f'Invalid schema: {e}')
            return func(*args, **kwargs)

        return wrapper

    return decorator


@contextlib.contextmanager
def save_tmpfile(blob: bytes, base_filename: str) -> Path:
    filename = TMP_UPLOAD_FOLDER / f'{uuid.uuid4()}_{secure_filename(base_filename)}'
    with open(filename, 'wb') as fd:
        fd.write(blob)

    try:
        yield filename
    finally:
        os.remove(filename)
