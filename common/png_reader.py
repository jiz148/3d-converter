"""
Png reader and processor for medical use
"""
import cv2
import os
import re

DEFAULT_PROPX = 420
DEFAULT_CROPY = 485
DEFAULT_PATH = '/home/bioprober/gh/3d-converter/Fusion'


class PngReader:

    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path

    def load_images_from_folder(self, cropx=DEFAULT_PROPX, cropy=DEFAULT_CROPY):
        images = []
        for filename in self.sorted_aphanumeric(os.listdir(self.path)):
            if filename.endswith('.png'):
                img = cv2.imread(os.path.join(self.path, filename))
                if cropx and cropy:
                    img = self._crop_center(img, cropx, cropy)
                if img is not None:
                    images.append(img)
        return images

    @staticmethod
    def _crop_center(img, cropx, cropy):
        y, x, c = img.shape
        startx = x // 2 - (cropx // 2)
        starty = y // 2 - (cropy // 2)
        return img[starty:starty + cropy, startx:startx + cropx]

    @staticmethod
    def sorted_aphanumeric(data):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(data, key=alphanum_key)
