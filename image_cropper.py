from PIL import Image

class ImageCropper():
    def __init__(self):
        self.image = None
        self.image_path = ''
    
    def set_image(self, image_path:str):
        self.image = Image.open(image_path)
        self.image_path = image_path
          
    def crop(self, values):
        if not self.image: return None
        left = values[0]
        top = values[1]
        right = values[2]
        bottom = values[3]
        box = (left, top, self.image.width - right, self.image.height - bottom)
        self.image = self.image.crop(box)
        self.image.save(self.image_path)