import math

MERIDIAN_LENGTH = 40_008_550  # метров
LON_METRES_PER_DEG = MERIDIAN_LENGTH / 360

EQUATOR_LENGTH = 40_075_696  # метров
LAT_METRES_PER_DEGREE_ON_EQUATOR = EQUATOR_LENGTH / 360


class CoordinatesCalculator:
    def __init__(self, base_bbox: tuple[float, float, float, float], image_size: tuple[int, int]):
        self.left_lon, self.top_lat, self.right_lon, self.bottom_lat = base_bbox
        self.image_width, self.image_height = image_size

    @property
    def width(self) -> float:
        return self.right_lon - self.left_lon

    @property
    def height(self) -> float:
        return self.top_lat - self.bottom_lat

    @property
    def w_units_per_pixel(self) -> float:
        return self.width / self.image_width

    @property
    def w_metres_per_pixel(self) -> float:
        return self.w_units_per_pixel * LON_METRES_PER_DEG

    @property
    def h_units_per_pixel(self) -> float:
        return self.height / self.image_height

    @property
    def h_metres_per_pixel(self) -> float:
        return self.h_units_per_pixel * LAT_METRES_PER_DEGREE_ON_EQUATOR * abs(math.cos(math.radians(self.top_lat)))

    def get_coordinates_of_bbox(self, bbox: tuple[int, int, int, int]) -> tuple[float, float, float, float]:
        x, y, w, h = bbox
        return (
            self.left_lon + x * self.w_units_per_pixel,
            self.top_lat - y * self.h_units_per_pixel,
            self.left_lon + (x + w) * self.w_units_per_pixel,
            self.top_lat - (y + h) * self.h_units_per_pixel,
        )

    def get_real_area(self, area_in_px: int) -> float:
        pixel_area = self.w_metres_per_pixel * self.h_metres_per_pixel
        return area_in_px * pixel_area
