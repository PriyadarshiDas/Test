import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from io import BytesIO
from zipfile import ZipFile
from xml.etree import ElementTree

def extract_images_and_ocr(file_bytes, filename):
    images_text = ""

    if filename.endswith(".pdf"):
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        for page in pdf:
            for img in page.get_images(full=True):
                base_image = pdf.extract_image(img[0])
                img_bytes = base_image["image"]
                img_pil = Image.open(BytesIO(img_bytes))
                images_text += pytesseract.image_to_string(img_pil)

    elif filename.endswith(".docx"):
        with BytesIO(file_bytes) as f:
            with ZipFile(f) as docx_zip:
                image_files = [name for name in docx_zip.namelist() if name.startswith("word/media/")]
                for image_name in image_files:
                    image_data = docx_zip.read(image_name)
                    try:
                        img_pil = Image.open(BytesIO(image_data))
                        images_text += pytesseract.image_to_string(img_pil)
                    except Exception as e:
                        print(f"Failed to process image {image_name}: {e}")
                        continue

    return images_text
