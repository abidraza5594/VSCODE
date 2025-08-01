#!/usr/bin/env python3
"""
Quick test script for browser functionality
"""

from finger import run_advanced_browser

def test_websites():
    """Test different websites"""
    
    websites = [
        ("Google", "https://www.google.com"),
        ("GitHub", "https://github.com"),
        ("Stack Overflow", "https://stackoverflow.com"),
        ("Augment Code", "https://www.augmentcode.com"),
        ("reCAPTCHA Demo", "https://www.google.com/recaptcha/api2/demo")
    ]
    
    print("🌐 QUICK WEBSITE TEST")
    print("="*30)
    
    for i, (name, url) in enumerate(websites, 1):
        print(f"{i}. {name} - {url}")
    
    choice = input("\n👉 Kaunsa website test karna hai? (1-5): ").strip()
    
    try:
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(websites):
            name, url = websites[choice_idx]
            print(f"\n🚀 Testing: {name}")
            print(f"🔗 URL: {url}")
            
            run_advanced_browser(
                device_type='desktop',
                browser_type='chrome',
                show_details=True,
                target_url=url
            )
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Invalid input!")

if __name__ == "__main__":
    test_websites()
