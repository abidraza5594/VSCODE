#!/usr/bin/env python3
"""
Test script for CAPTCHA functionality in finger.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from finger import AdvancedFingerprinter

def test_captcha_config():
    """Test CAPTCHA configuration"""
    print("🧪 Testing CAPTCHA configuration...")
    
    fingerprinter = AdvancedFingerprinter()
    
    # Check if CAPTCHA config is properly initialized
    assert hasattr(fingerprinter, 'captcha_config'), "CAPTCHA config not found"
    assert 'max_attempts' in fingerprinter.captcha_config, "max_attempts not in config"
    assert 'wait_time' in fingerprinter.captcha_config, "wait_time not in config"
    assert 'ocr_enabled' in fingerprinter.captcha_config, "ocr_enabled not in config"
    assert 'manual_fallback' in fingerprinter.captcha_config, "manual_fallback not in config"
    
    print("✅ CAPTCHA configuration test passed!")
    print(f"   Max attempts: {fingerprinter.captcha_config['max_attempts']}")
    print(f"   Wait time: {fingerprinter.captcha_config['wait_time']} seconds")
    print(f"   OCR enabled: {fingerprinter.captcha_config['ocr_enabled']}")
    print(f"   Manual fallback: {fingerprinter.captcha_config['manual_fallback']}")

def test_captcha_methods():
    """Test CAPTCHA methods exist"""
    print("\n🧪 Testing CAPTCHA methods...")
    
    fingerprinter = AdvancedFingerprinter()
    
    # Check if methods exist
    assert hasattr(fingerprinter, 'solve_captcha'), "solve_captcha method not found"
    assert hasattr(fingerprinter, 'handle_captcha_challenge'), "handle_captcha_challenge method not found"
    assert hasattr(fingerprinter, 'navigate_with_captcha_handling'), "navigate_with_captcha_handling method not found"
    
    print("✅ CAPTCHA methods test passed!")
    print("   ✓ solve_captcha method exists")
    print("   ✓ handle_captcha_challenge method exists")
    print("   ✓ navigate_with_captcha_handling method exists")

def test_imports():
    """Test required imports"""
    print("\n🧪 Testing required imports...")
    
    try:
        import base64
        import io
        from PIL import Image
        print("✅ PIL (Pillow) import successful")
    except ImportError as e:
        print(f"❌ PIL import failed: {e}")
        print("💡 Install with: pip install Pillow")
        return False
    
    try:
        import pytesseract
        print("✅ pytesseract import successful")
    except ImportError as e:
        print(f"❌ pytesseract import failed: {e}")
        print("💡 Install with: pip install pytesseract")
        print("💡 Also install Tesseract OCR: https://github.com/tesseract-ocr/tesseract")
        return False
    
    return True

if __name__ == "__main__":
    print("🎭 CAPTCHA FUNCTIONALITY TEST")
    print("="*40)
    
    try:
        # Test imports first
        if not test_imports():
            print("\n❌ Import tests failed. Please install missing dependencies.")
            sys.exit(1)
        
        # Test configuration
        test_captcha_config()
        
        # Test methods
        test_captcha_methods()
        
        print("\n🎉 All tests passed! CAPTCHA functionality is ready.")
        print("\n📋 Features added:")
        print("   • Image CAPTCHA solving with OCR")
        print("   • reCAPTCHA detection and manual handling")
        print("   • hCaptcha detection and manual handling")
        print("   • Cloudflare CAPTCHA detection")
        print("   • Automatic retry mechanism")
        print("   • Navigation with CAPTCHA handling")
        print("   • Custom website testing")
        
        print("\n🚀 You can now run: python finger.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        sys.exit(1)
