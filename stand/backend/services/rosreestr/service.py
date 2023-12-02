from functools import cached_property

from rosreestr_api.clients import PKKRosreestrAPIClient


class RosreestrService:

    @cached_property
    def client(self):
        return PKKRosreestrAPIClient()


if __name__ == '__main__':
    service = RosreestrService()
    buildings = service.client.get_building_by_coordinates(long=37, lat=55)
    print(buildings)
