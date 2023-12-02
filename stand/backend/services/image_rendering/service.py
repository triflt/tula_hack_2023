from functools import cached_property

from PIL import Image, ImageDraw, ImageFont


class ImageRenderer:
    def __init__(self, image: Image.Image):
        self.image = image

    @cached_property
    def draw(self) -> ImageDraw.ImageDraw:
        return ImageDraw.Draw(self.image)

    def draw_rect(
            self,
            bbox: tuple[int, int, int, int],
            fill: tuple[int, int, int] | None = None,
            outline: tuple[int, int, int] | None = None,
            width: int = 1,
    ) -> None:
        x, y, w, h = bbox
        self.draw.rectangle((x, y, x + w, y + h), fill=fill, outline=outline, width=width)

    def draw_text(
            self,
            xy: tuple[int, int],
            text: str,
    ) -> None:
        self.draw.text(xy, text, font=self.font)

    @cached_property
    def font(self) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(
            'stand/backend/services/image_rendering/static/Roboto-Regular.ttf',
            size=min(16, min(self.image.size) // 32),
            encoding='UTF-8',
        )
