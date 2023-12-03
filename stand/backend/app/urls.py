import base64
from io import BytesIO

from flask import Blueprint, jsonify, request
from PIL import Image

from stand.backend.app.config import BUILDING_COLORS, MIN_BUILDING_AREA
from stand.backend.app.utils import save_tmpfile, validate_json
from stand.backend.services.classification.service import Classificator
from stand.backend.services.classification.config import DEFAULT_CONFIG
from stand.backend.services.classification.typing import Buildings
from stand.backend.services.coordinates_calculator.service import CoordinatesCalculator
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
        coords_calculator = CoordinatesCalculator(
            base_bbox=(
                request.json['bbox']['left_lon'],
                request.json['bbox']['top_lat'],
                request.json['bbox']['right_lon'],
                request.json['bbox']['bottom_lat'],
            ),
            image_size=image_renderer.image.size,
        ) if 'bbox' in request.json else None
        buildings_json = []
        idx = 0
        for item in classificator.classification_result:
            if item['area'] < MIN_BUILDING_AREA:
                continue
            building_type = Buildings(item['class'])
            if building_type == Buildings.NOTHING:
                continue
            idx += 1
            bbox = item['bbox']
            image_renderer.draw_rect(bbox, outline=BUILDING_COLORS[building_type], width=3)
            image_renderer.draw_text(bbox[:2], str(idx))
            building_json = {
                'idx': idx,
                'bbox': bbox,
                'type': building_type.verbose_name,
                'area_in_px': item['area'],
            }
            if coords_calculator:
                building_json['coordinates_bbox'] = coords_calculator.get_coordinates_of_bbox(bbox)
                building_json['area_in_metres'] = coords_calculator.get_real_area(item['area'])

            buildings_json.append(building_json)

        io = BytesIO()
        image_renderer.image.save(io, format=filename.suffix.removeprefix('.').upper().replace('JPG', 'JPEG'))
        return jsonify({
            'image': base64.b64encode(io.getvalue()).decode('ascii'),
            'buildings': buildings_json,
        })
