import easyocr
import os
import json
import sys
import warnings
import logging
import ctypes
from pdf2image import convert_from_path
from tempfile import TemporaryDirectory

# Suppress warnings and unnecessary logging
warnings.filterwarnings("ignore")
logging.getLogger('torch').setLevel(logging.ERROR)

# Suppress stderr for cleaner execution
libc = ctypes.CDLL(None)
stderr_fileno = sys.stderr.fileno()
original_stderr = os.dup(stderr_fileno)
os.close(stderr_fileno)
os.open(os.devnull, os.O_RDWR)

# Define cache directories (Replace with user-specific paths if needed)
cache_dir = os.path.join(os.getcwd(), "easyocr_cache")
transformers_cache_dir = os.path.join(os.getcwd(), "huggingface_cache")

# Ensure cache directories exist
os.makedirs(cache_dir, exist_ok=True)
os.makedirs(transformers_cache_dir, exist_ok=True)

# Set environment variables for EasyOCR and Huggingface
os.environ['HOME'] = cache_dir
os.environ['EASYOCR_CACHE_DIR'] = cache_dir
os.environ['TRANSFORMERS_CACHE'] = transformers_cache_dir

def ocr_image(image_path):
    """
    Performs OCR on an image file using EasyOCR.

    Args:
        image_path (str): Path to the image file.

    Returns:
        dict: OCR results in JSON format.
    """
    try:
        if not os.path.exists(image_path):
            return {"status": "error", "message": f"Error: The file {image_path} does not exist."}

        # Initialize EasyOCR reader
        reader = easyocr.Reader(
            ['en'],  # Language: English
            gpu=True,  # Use GPU for faster processing if available
            model_storage_directory=cache_dir,
            user_network_directory=cache_dir,
            recog_network='english_g2',  # Use the English model
            download_enabled=False,
            verbose=False
        )

        # Perform OCR
        result = reader.readtext(image_path, detail=0)

        if not result:
            return {"status": "error", "message": "No text detected in the image."}

        text = "\n".join(result)
        return {"status": "success", "text": text}

    except Exception as e:
        return {"status": "error", "message": f"Error processing image: {str(e)}"}

    finally:
        # Restore the original stderr
        os.dup2(original_stderr, stderr_fileno)

def ocr_pdf(pdf_path):
    """
    Performs OCR on a PDF file by converting it to images first.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        dict: OCR results in JSON format.
    """
    try:
        if not os.path.exists(pdf_path):
            return {"status": "error", "message": f"Error: The file {pdf_path} does not exist."}

        text_output = []

        # Convert PDF pages to images
        with TemporaryDirectory() as temp_dir:
            images = convert_from_path(pdf_path, output_folder=temp_dir)

            # Initialize EasyOCR reader
            reader = easyocr.Reader(
                ['en'],
                gpu=False,  # GPU is not required for PDF processing
                model_storage_directory=cache_dir,
                user_network_directory=cache_dir,
                recog_network='english_g2',
                download_enabled=False,
                verbose=False
            )

            # Process each page image
            for i, image in enumerate(images):
                image_path = os.path.join(temp_dir, f'temp_page_{i}.png')
                image.save(image_path, 'PNG')

                result = reader.readtext(image_path, detail=0)

                if result:
                    text_output.append("\n".join(result))

        if not text_output:
            return {"status": "error", "message": "No text detected in the PDF."}

        return {"status": "success", "text": "\n".join(text_output)}

    except Exception as e:
        return {"status": "error", "message": f"Error processing PDF: {str(e)}"}

def main(file_path):
    """
    Determines the file type and processes it accordingly.

    Args:
        file_path (str): Path to the input file.

    Prints:
        JSON output with OCR results.
    """
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.pdf':
        result = ocr_pdf(file_path)
    else:
        result = ocr_image(file_path)

    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    """
    Command-line execution of the script.
    Usage:
        python3 ocr_script.py <file_path>
    """
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No file path provided"}, indent=4))
    else:
        main(sys.argv[1])
