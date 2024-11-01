from PIL import Image, ImageOps
import io
from fastapi import UploadFile


class PictureService:

    async def process_image(self, upload_file: UploadFile):
        contents = await upload_file.read()
        image = Image.open(io.BytesIO(contents))
        resized_images = self.resize_image(image)
        grayscale_image = self.convert_to_grayscale(resized_images)

        return grayscale_image

    @staticmethod
    def resize_image(image):
        width, height = image.size
        resized_images = {}

        if width <= 200 and height <= 200:
            size = (100, 100)
        elif width <= 800 and height <= 600:
            size = (500, 500)
        else:
            size = (1000, 1000)

        resized_image = ImageOps.fit(image, size)
        return resized_image

    @staticmethod
    def convert_to_grayscale(image):
        return ImageOps.grayscale(image)

async def create_picture_service() -> PictureService:
    return PictureService()







