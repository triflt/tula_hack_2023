from stand.backend.services.classification.typing import Buildings

BUILDING_COLORS: dict[Buildings, tuple[int, int, int]] = {
    Buildings.GREENHOUSE: (124, 252, 0),
    Buildings.PRIVATE_HOUSE: (204, 102, 0),
    Buildings.PUBLIC_BUILDING: (31, 174, 233),
    Buildings.PUBLIC_HOUSE: (125, 127, 125),
    Buildings.BARN: (248, 243, 43),
    Buildings.POOL: (0, 0, 255),
    Buildings.NOTHING: (0, 0, 0),
}
