# must install pytesseract
from pathlib import Path
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img_path = Path(r"C:\Users\foo\Downloads\bar.PNG")
img = Image.open(img_path)
text = pytesseract.image_to_string(img)
print(text)
