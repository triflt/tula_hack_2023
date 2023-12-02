import base64
from io import BytesIO

from flask import Blueprint, jsonify, request
from PIL import Image

from stand.backend.app.config import BUILDING_COLORS
from stand.backend.app.utils import save_tmpfile, validate_json
from stand.backend.services.classification.service import Classificator
from stand.backend.services.classification.config import DEFAULT_CONFIG
from stand.backend.services.classification.typing import Buildings
from stand.backend.services.image_rendering.service import ImageRenderer

urls = Blueprint('app', __name__, url_prefix='/api/v1')


@urls.route('/markup', methods=['POST'])
@validate_json('markup_handler_schema.json')
def markup_handler():
    with save_tmpfile(
        base64.b64decode(request.json['image']['base64data'].encode('ascii')),
        request.json['image']['filename'],
    ) as filename:
        classificator = Classificator(filename, config=DEFAULT_CONFIG)
        image_renderer = ImageRenderer(Image.open(filename))
        building_json = []
        for item in classificator.classification_result:
            building_type = Buildings(item['class'])
            bbox = item['bbox']
            image_renderer.draw_rect(bbox, outline=BUILDING_COLORS[building_type], width=3)
            image_renderer.draw_text(bbox[:2], building_type.verbose_name)
            building_json.append({
                'bbox': bbox,
                'type': building_type.verbose_name,
            })

        io = BytesIO()
        image_renderer.image.save(io, format=filename.suffix.removeprefix('.').upper().replace('JPG', 'JPEG'))
        return jsonify({
            'image': base64.b64encode(io.getvalue()).decode('ascii'),
            'buildings': building_json,
        })
