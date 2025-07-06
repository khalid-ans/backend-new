import pytesseract
from PIL import Image
import io
import logging
import os

logger = logging.getLogger(__name__)

# Configure Tesseract path for Windows
if os.name == 'nt':  # Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(file):
    try:
        # Reset file pointer to beginning
        file.seek(0)
        
        # Open and validate image
        image = Image.open(io.BytesIO(file.read()))
        
        # Convert to RGB if necessary (tesseract works better with RGB)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Extract text using pytesseract
        text = pytesseract.image_to_string(image)
        
        logger.info(f"OCR extracted {len(text)} characters")
        return text
        
    except Exception as e:
        logger.error(f"OCR processing failed: {str(e)}")
        raise Exception(f"Failed to process image: {str(e)}") 