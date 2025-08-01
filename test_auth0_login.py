#!/usr/bin/env python3
"""
Auth0 Login Test Script
"""

from finger import run_advanced_browser

def test_auth0_login():
    """Test Auth0 login functionality"""
    
    print("🔐 AUTH0 LOGIN TEST")
    print("="*30)
    
    # Auth0 login URL
    login_url = "https://login.augmentcode.com/u/login/identifier?state=hKFo2SBiUElHWWFaNVUyTkZiLXNUX0luTTlMcnBQTUFoMmFUSaFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIFpSNVg4eWp2WE5vRkhFeW0zY2Q3UUo3RXUzNTE0QUowo2NpZNkgd2xMVFZXR0RmSXRXOUh6aUlvd1NSaWVRTlJ5bE1QVGE"
    
    print(f"🔗 Login URL: {login_url}")
    print()
    print("📋 Test Steps:")
    print("1. Browser launch hoga")
    print("2. Auth0 login page load hoga")
    print("3. Agar redirect ho jaye to manual navigation kar sakte hain")
    print("4. Login form manually fill kar sakte hain")
    print()
    
    input("👉 Test start karne ke liye Enter dabayein...")
    
    try:
        run_advanced_browser(
            device_type='desktop',
            browser_type='chrome',
            show_details=True,
            target_url=login_url
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_manual_navigation():
    """Test manual navigation to login page"""
    
    print("🔧 MANUAL NAVIGATION TEST")
    print("="*35)
    
    print("📋 Manual Steps:")
    print("1. Browser launch hoga with home page")
    print("2. Manually login button click kariye")
    print("3. Auth0 login page par navigate kariye")
    print("4. Login form fill kariye")
    print()
    
    input("👉 Manual test start karne ke liye Enter dabayein...")
    
    try:
        # Start with home page
        run_advanced_browser(
            device_type='desktop',
            browser_type='chrome',
            show_details=True,
            target_url="https://www.augmentcode.com"
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🎯 AUTH0 LOGIN TEST OPTIONS")
    print("="*35)
    print("1. 🔐 Direct Auth0 URL test")
    print("2. 🔧 Manual navigation test")
    print("3. ❌ Exit")
    
    choice = input("\n👉 Apna choice enter karo (1-3): ").strip()
    
    if choice == '1':
        test_auth0_login()
    elif choice == '2':
        test_manual_navigation()
    elif choice == '3':
        print("👋 Bye!")
    else:
        print("❌ Invalid choice!")
