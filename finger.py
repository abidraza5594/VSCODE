import random
import string
from playwright.sync_api import sync_playwright
import time

def random_user_agent():
    versions = {
        'Chrome': [
            f'{random.randint(90, 124)}.0.{random.randint(1000, 9999)}.{random.randint(10, 200)}',
            f'{random.randint(90, 124)}.0.{random.randint(1000, 9999)}.{random.randint(10, 200)}'
        ],
        'Firefox': [f'{random.randint(90, 124)}.0', f'{random.randint(90, 124)}.0']
    }
    os_types = [
        ('Windows NT 10.0; Win64; x64', 'Windows 10'),
        ('Windows NT 11.0; Win64; x64', 'Windows 11'),
        ('Macintosh; Intel Mac OS X 10_15_7', 'Mac OS X'),
        ('X11; Linux x86_64', 'Linux'),
        ('X11; Ubuntu; Linux x86_64', 'Ubuntu')
    ]
    
    browser = random.choice(['Chrome', 'Firefox'])
    os_type, os_name = random.choice(os_types)
    
    if browser == 'Chrome':
        return f'Mozilla/5.0 ({os_type}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{versions["Chrome"][0]} Safari/537.36', os_name
    else:
        return f'Mozilla/5.0 ({os_type}; rv:{versions["Firefox"][0]}) Gecko/20100101 Firefox/{versions["Firefox"][1]}', os_name

def random_screen_resolution():
    resolutions = [
        {'width': 1920, 'height': 1080},
        {'width': 1366, 'height': 768},
        {'width': 1536, 'height': 864},
        {'width': 1440, 'height': 900},
        {'width': 1600, 'height': 900},
    ]
    return random.choice(resolutions)

def generate_random_email():
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'protonmail.com', 'mail.com']
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(8, 12)))
    return f"{username}@{random.choice(domains)}"

def run_browser():
    with sync_playwright() as p:
        # Randomize browser fingerprint
        user_agent, platform = random_user_agent()
        screen = random_screen_resolution()
        timezone = random.choice(['America/New_York', 'Europe/London', 'Asia/Kolkata', 'Australia/Sydney'])
        locale = random.choice(['en-US', 'en-GB', 'en-IN', 'en-AU'])
        
        browser = p.chromium.launch(
            headless=False,
            args=[
                f'--user-agent={user_agent}',
                f'--window-size={screen["width"]},{screen["height"]}',
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-extensions',
                '--disable-popup-blocking',
                f'--lang={locale.split("-")[0]}'
            ]
        )
        
        context = browser.new_context(
            user_agent=user_agent,
            viewport={'width': screen['width'], 'height': screen['height']},
            locale=locale,
            timezone_id=timezone,
            permissions=[],
            color_scheme='light',
            device_scale_factor=random.uniform(0.8, 1.5)
        )  # <-- यहाँ closing parenthesis जोड़ा गया है
        
        page = context.new_page()
        
        try:
            print("Augment वेबसाइट पर जा रहे हैं...")
            page.goto('https://www.augmentcode.com/', timeout=30000)
            page.wait_for_selector('body', timeout=15000)
            
            if "augment" not in page.title().lower():
                print("चेतावनी: हो सकता है Augment की वेबसाइट न लोड हुई हो")
            else:
                print("Augment वेबसाइट सफलतापूर्वक लोड हुई")
                
        except Exception as e:
            print(f"त्रुटि: {str(e)}")
            print("आप मैन्युअली ब्राउज़र का उपयोग कर सकते हैं")
        
        print("\nब्राउज़र फिंगरप्रिंट विवरण:")
        print(f"यूजर एजेंट: {user_agent}")
        print(f"प्लेटफॉर्म: {platform}")
        print(f"रिज़ॉल्यूशन: {screen['width']}x{screen['height']}")
        print(f"टाइमजोन: {timezone}")
        print(f"भाषा: {locale}\n")
        
        print("अब आप मैन्युअली:")
        print("1. साइनअप पेज पर जा सकते हैं")
        print("2. नया अकाउंट बना सकते हैं")
        print("3. एक्सटेंशन का उपयोग कर सकते हैं\n")
        
        input("ब्राउज़र बंद करने के लिए एंटर दबाएं...")
        browser.close()

if __name__ == "__main__":
    run_browser()