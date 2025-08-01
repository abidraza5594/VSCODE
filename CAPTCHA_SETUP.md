# CAPTCHA Functionality Setup Guide

## 🎯 Overview
Your `finger.py` file has been enhanced with comprehensive CAPTCHA solving capabilities including:

- **Image CAPTCHA solving** with OCR (Optical Character Recognition)
- **reCAPTCHA detection** and manual handling
- **hCaptcha detection** and manual handling  
- **Cloudflare CAPTCHA detection**
- **Automatic retry mechanism**
- **Navigation with CAPTCHA handling**
- **Custom website testing**

## 📦 Required Dependencies

### 1. Install Python packages:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install playwright>=1.40.0
pip install Pillow>=10.0.0
pip install pytesseract>=0.3.10
```

### 2. Install Tesseract OCR Engine:

#### Windows:
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install the executable
3. Add to PATH or set TESSDATA_PREFIX environment variable

#### Alternative Windows (using chocolatey):
```bash
choco install tesseract
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install tesseract-ocr
```

#### macOS:
```bash
brew install tesseract
```

### 3. Install Playwright browsers:
```bash
playwright install
```

## 🚀 Usage

### Basic Usage:
```bash
python finger.py
```

### Menu Options:
1. **Single browser launch** - Random device with CAPTCHA handling
2. **Specific device type** - Choose desktop/mobile/tablet
3. **Multiple browsers** - Launch multiple instances
4. **Available devices** - View all device profiles
5. **Custom website test** - Test any website with CAPTCHA handling
6. **Exit**

### Custom Website Testing:
```python
# Example: Test a website with CAPTCHA
python finger.py
# Choose option 5
# Enter URL: https://example.com/login
```

## 🔧 CAPTCHA Configuration

The CAPTCHA solver can be configured in the `AdvancedFingerprinter` class:

```python
self.captcha_config = {
    'max_attempts': 3,        # Maximum solve attempts
    'wait_time': 5,          # Wait time between attempts (seconds)
    'ocr_enabled': True,     # Enable OCR for image CAPTCHAs
    'manual_fallback': True  # Allow manual solving
}
```

## 🎭 CAPTCHA Types Supported

### 1. Image CAPTCHAs
- Automatically detected by image selectors
- Uses OCR (pytesseract) to extract text
- Supports base64 encoded images
- Manual fallback for complex images

### 2. reCAPTCHA
- Detects reCAPTCHA iframes
- Provides manual solving option
- Waits for user completion

### 3. hCaptcha
- Detects hCaptcha iframes
- Manual solving with user interaction

### 4. Cloudflare CAPTCHAs
- Detects Cloudflare challenge pages
- Manual solving support

### 5. Text-based CAPTCHAs
- Detects CAPTCHA input fields
- Manual entry option

## 🔍 How It Works

1. **Navigation**: Enhanced navigation with automatic CAPTCHA detection
2. **Detection**: Scans page for various CAPTCHA types using CSS selectors
3. **Solving**: Attempts automatic solving (OCR) or manual fallback
4. **Retry**: Automatic retry mechanism with configurable attempts
5. **Verification**: Checks if CAPTCHA was successfully solved

## 🛠️ Troubleshooting

### Common Issues:

1. **Tesseract not found**:
   - Ensure Tesseract is installed and in PATH
   - Set TESSDATA_PREFIX environment variable

2. **OCR accuracy issues**:
   - Some CAPTCHAs are intentionally difficult
   - Manual fallback will be triggered
   - Consider adjusting OCR configuration

3. **Browser detection**:
   - Some sites may still detect automation
   - The fingerprinting helps but isn't 100% foolproof

### Testing:
```bash
python test_captcha.py
```

## 📝 Example Code

```python
from finger import AdvancedFingerprinter

# Create fingerprinter with CAPTCHA support
fingerprinter = AdvancedFingerprinter()

# Test with custom website
fingerprinter.run_advanced_browser(
    device_type='desktop',
    browser_type='chrome', 
    target_url='https://example.com'
)
```

## ⚠️ Important Notes

- **Legal Use**: Only use on websites you own or have permission to test
- **Rate Limiting**: Respect website rate limits and terms of service
- **Manual Fallback**: Complex CAPTCHAs may require manual solving
- **Detection**: Some advanced anti-bot systems may still detect automation

## 🎉 Features Added

✅ **Image CAPTCHA solving** with OCR  
✅ **Multiple CAPTCHA type detection**  
✅ **Automatic retry mechanism**  
✅ **Manual fallback options**  
✅ **Enhanced navigation**  
✅ **Custom website testing**  
✅ **Comprehensive error handling**  

Your browser fingerprinting tool is now equipped with advanced CAPTCHA handling capabilities!
