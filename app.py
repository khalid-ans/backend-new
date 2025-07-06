from flask import Flask, request, jsonify
from flask_cors import CORS
from ocr import extract_text
from parser import extract_medicines
from scraper import get_price
import traceback
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Get allowed origins from environment variable or use defaults
# Update this with your actual frontend URL
allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'https://frontend-dzuh.vercel.app').split(',')
CORS(app, origins=allowed_origins, supports_credentials=True)

@app.route('/')
def health():
    return jsonify({'status': 'Backend is running'})

@app.route('/test-upload', methods=['POST'])
def test_upload():
    """Test endpoint that doesn't require OCR"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        logger.info(f"Test upload received file: {file.filename}")
        
        # Return mock data for testing
        mock_data = {
            'items': [
                {'medicine': 'Paracetamol 500mg', 'price': '₹15'},
                {'medicine': 'Amoxicillin 250mg', 'price': '₹45'},
                {'medicine': 'Omeprazole 20mg', 'price': '₹120'}
            ],
            'total': 180
        }
        
        return jsonify(mock_data)
        
    except Exception as e:
        logger.error(f"Test upload error: {str(e)}")
        return jsonify({'error': 'Test upload failed'}), 500

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Check if file is present in request
        if 'image' not in request.files:
            logger.error("No image file in request")
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        # Check if file is empty
        if file.filename == '':
            logger.error("No file selected")
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file type
        if not file.content_type.startswith('image/'):
            logger.error(f"Invalid file type: {file.content_type}")
            return jsonify({'error': 'Please upload an image file'}), 400
        
        logger.info(f"Processing file: {file.filename}")
        
        # Extract text from image
        try:
            text = extract_text(file)
            logger.info(f"Extracted text length: {len(text)}")
            if not text.strip():
                logger.warning("No text extracted from image")
                return jsonify({'error': 'No text could be extracted from the image. Please ensure the image is clear and contains readable text.'}), 400
        except Exception as e:
            logger.error(f"OCR error: {str(e)}")
            return jsonify({'error': 'Failed to process image. Please ensure the image is clear and readable.'}), 500
        
        # Extract medicines from text
        try:
            medicines = extract_medicines(text)
            logger.info(f"Found {len(medicines)} medicines: {medicines}")
            if not medicines:
                return jsonify({'error': 'No medicines found in the image. Please ensure the prescription contains medicine names.'}), 400
        except Exception as e:
            logger.error(f"Parser error: {str(e)}")
            return jsonify({'error': 'Failed to parse medicines from text.'}), 500
        
        # Get prices for medicines
        result = []
        total = 0
        
        for med in medicines:
            try:
                price = get_price(med)
                logger.info(f"Price for {med}: {price}")
                
                # Extract numeric price value
                try:
                    price_val = int(price.replace('₹', '').replace(',', '').split('.')[0])
                except:
                    price_val = 0
                
                total += price_val
                result.append({'medicine': med, 'price': price})
                
            except Exception as e:
                logger.error(f"Price lookup error for {med}: {str(e)}")
                result.append({'medicine': med, 'price': '₹0'})
        
        logger.info(f"Processing complete. Total: ₹{total}")
        return jsonify({'items': result, 'total': total})
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'An unexpected error occurred. Please try again.'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 