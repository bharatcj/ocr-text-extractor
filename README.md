### OCR Text Extractor

A Python script that extracts text from **images and PDFs** using **EasyOCR**.  
Supports **GPU acceleration** for faster processing and provides **structured JSON output** for easy integration.

## 🚀 Features
- **Extract text** from images (`.jpg`, `.png`, `.bmp`, etc.).
- **Convert PDFs** to images and perform OCR.
- **Supports GPU acceleration** for faster processing.
- **Handles errors gracefully**, ensuring robust performance.
- **Returns results in structured JSON format**.

---

## 🔧 **Installation**

### **1. Install Python and Required Libraries**
Ensure Python is installed. If not, download it from [Python.org](https://www.python.org/downloads/).

Then, install the required dependencies:

```sh
pip3 install easyocr pdf2image pillow
```

Additionally, install **Poppler** for PDF-to-image conversion:

#### **Windows**
1. Download **Poppler for Windows**: [Download Here](https://github.com/oschwartz10612/poppler-windows/releases/)
2. Extract it and **add the `bin` folder to system PATH**.
3. Verify installation:
   ```sh
   where poppler
   ```

#### **Linux (Ubuntu)**
```sh
sudo apt update
sudo apt install poppler-utils
```

#### **Mac (Homebrew)**
```sh
brew install poppler
```

---

## 🎯 **Running the Script**
### **Step 1: Clone the Repository**
```sh
git clone https://github.com/bharatcj/ocr-text-extractor.git
cd ocr-text-extractor
```

### **Step 2: Run the Script**
```sh
python3 ocr_script.py <file_path>
```
Replace `<file_path>` with the path to your image or PDF.

**Example:**
```sh
python3 ocr_script.py example.jpg
python3 ocr_script.py document.pdf
```

---

## 📜 **Example Output**
### **For an Image**
```json
{
    "status": "success",
    "text": "Extracted text from the image."
}
```
### **For a PDF**
```json
{
    "status": "success",
    "text": "Extracted text from all PDF pages."
}
```

---

## ⚠️ **Error Handling**
If an error occurs:
- The script prints a **detailed error message**.
- It verifies **file existence** before processing.
- Returns **formatted JSON responses** for easy debugging.

---

## 🔄 **Customization**
- Modify `ocr_script.py` to enable **multi-language detection** (change `['en']` to `['en', 'fr', 'es']`).
- Adjust **GPU settings** if required (`gpu=True` or `gpu=False`).

---

## 🛡️ **License**
This project is licensed under the **MIT License**.

---

## 🤝 **Contributing**
Contributions are welcome! Feel free to **fork this repository** and submit pull requests.

---

### **Author**
Developed by **Bharat CJ**  
GitHub: https://github.com/bharatcj

---

💡 **Did you know?** EasyOCR supports over **80 languages**, making it perfect for global applications! 🌍🚀