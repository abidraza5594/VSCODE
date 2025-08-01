#!/usr/bin/env python3
"""
CAPTCHA Demo Script - Test CAPTCHA functionality
"""

import os
import sys
from finger import AdvancedFingerprinter, run_advanced_browser

def test_captcha_website():
    """Test CAPTCHA functionality with local HTML file"""
    
    # Get the absolute path to the test HTML file
    html_file = os.path.abspath("test_captcha_website.html")
    file_url = f"file:///{html_file.replace(os.sep, '/')}"
    
    print("🎭 CAPTCHA FUNCTIONALITY DEMO")
    print("="*50)
    print(f"📁 Test file: {html_file}")
    print(f"🌐 URL: {file_url}")
    print()
    
    if not os.path.exists(html_file):
        print("❌ Test HTML file not found!")
        print("💡 Run this script from the same directory as test_captcha_website.html")
        return False
    
    print("🚀 Starting browser with CAPTCHA detection...")
    
    # Create fingerprinter instance
    fingerprinter = AdvancedFingerprinter()
    
    # Run browser with test website
    try:
        run_advanced_browser(
            device_type='desktop',
            browser_type='chrome',
            show_details=True,
            target_url=file_url
        )
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_real_captcha_websites():
    """Test with real websites that might have CAPTCHAs"""
    
    websites_with_captcha = [
        "https://www.google.com/recaptcha/api2/demo",  # reCAPTCHA demo
        "https://captcha.com/demos/features/captcha-demo.aspx",  # CAPTCHA demo
        "https://www.hcaptcha.com/",  # hCaptcha
    ]
    
    print("🌐 REAL CAPTCHA WEBSITES TEST")
    print("="*40)
    
    for i, url in enumerate(websites_with_captcha, 1):
        print(f"\n{i}. {url}")
    
    choice = input("\n👉 Kaunsa website test karna hai? (1-3): ").strip()
    
    try:
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(websites_with_captcha):
            selected_url = websites_with_captcha[choice_idx]
            print(f"\n🚀 Testing: {selected_url}")
            
            run_advanced_browser(
                device_type='desktop',
                browser_type='chrome',
                show_details=True,
                target_url=selected_url
            )
            return True
        else:
            print("❌ Invalid choice!")
            return False
    except ValueError:
        print("❌ Invalid input!")
        return False

if __name__ == "__main__":
    print("🎯 CAPTCHA DEMO OPTIONS")
    print("="*30)
    print("1. 🏠 Test local CAPTCHA website")
    print("2. 🌐 Test real CAPTCHA websites")
    print("3. ❌ Exit")
    
    choice = input("\n👉 Apna choice enter karo (1-3): ").strip()
    
    if choice == '1':
        test_captcha_website()
    elif choice == '2':
        test_real_captcha_websites()
    elif choice == '3':
        print("👋 Bye!")
    else:
        print("❌ Invalid choice!")
