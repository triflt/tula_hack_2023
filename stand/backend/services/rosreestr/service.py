import requests


class RosreestrService:
    BASE_URL = 'http://pkk.rosreestr.ru/api'
    SEARCH_BUILDING_BY_COORDINATES = BASE_URL + '/features/5?text={lat}%20{long}&limit={limit}&tolerance={tolerance}'

    def get_building_by_coordinates(self, lat: float, long: float) -> dict | None:
        response = requests.get(self.SEARCH_BUILDING_BY_COORDINATES.format(lat=lat, long=long, limit=1, tolerance=2),
                                verify=False)
        response_data = response.json()
        return response_data['features'][0] if response_data['total'] else None
