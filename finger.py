import random
import string
import json
import hashlib
import uuid
from playwright.sync_api import sync_playwright
import time
from datetime import datetime, timedelta
import base64
import io
from PIL import Image
import pytesseract  # For OCR-based CAPTCHA solving

class AdvancedFingerprinter:
    def __init__(self):
        self.device_profiles = self._load_device_profiles()
        self.browser_versions = self._get_latest_browser_versions()

        # CAPTCHA solving configuration
        self.captcha_config = {
            'max_attempts': 3,
            'wait_time': 5,
            'ocr_enabled': True,
            'manual_fallback': True
        }

    def _load_device_profiles(self):
        """Different device profiles load karte hain"""
        return {
            'desktop': {
                'windows_10': {
                    'os': 'Windows NT 10.0; Win64; x64',
                    'platform': 'Win32',
                    'resolutions': [
                        {'width': 1920, 'height': 1080, 'ratio': 1.0},
                        {'width': 2560, 'height': 1440, 'ratio': 1.0},
                        {'width': 3840, 'height': 2160, 'ratio': 1.0},
                        {'width': 1366, 'height': 768, 'ratio': 1.0},
                        {'width': 1536, 'height': 864, 'ratio': 1.25},
                        {'width': 1600, 'height': 900, 'ratio': 1.0},
                        {'width': 1440, 'height': 900, 'ratio': 1.0},
                        {'width': 2048, 'height': 1152, 'ratio': 1.0}
                    ],
                    'memory': [4, 8, 16, 32],
                    'cores': [2, 4, 6, 8, 12, 16]
                },
                'windows_11': {
                    'os': 'Windows NT 10.0; Win64; x64',
                    'platform': 'Win32',
                    'resolutions': [
                        {'width': 1920, 'height': 1080, 'ratio': 1.0},
                        {'width': 2560, 'height': 1440, 'ratio': 1.0},
                        {'width': 3840, 'height': 2160, 'ratio': 1.0},
                        {'width': 1366, 'height': 768, 'ratio': 1.0},
                        {'width': 2560, 'height': 1600, 'ratio': 1.0}
                    ],
                    'memory': [8, 16, 32, 64],
                    'cores': [4, 6, 8, 12, 16, 20]
                },
                'macos_monterey': {
                    'os': 'Macintosh; Intel Mac OS X 10_15_7',
                    'platform': 'MacIntel',
                    'resolutions': [
                        {'width': 1440, 'height': 900, 'ratio': 2.0},
                        {'width': 1680, 'height': 1050, 'ratio': 2.0},
                        {'width': 1920, 'height': 1200, 'ratio': 2.0},
                        {'width': 2560, 'height': 1600, 'ratio': 2.0},
                        {'width': 2880, 'height': 1800, 'ratio': 2.0}
                    ],
                    'memory': [8, 16, 32, 64],
                    'cores': [4, 6, 8, 10, 12]
                },
                'macos_ventura': {
                    'os': 'Macintosh; Intel Mac OS X 10_15_7',
                    'platform': 'MacIntel',
                    'resolutions': [
                        {'width': 1512, 'height': 982, 'ratio': 2.0},
                        {'width': 1728, 'height': 1117, 'ratio': 2.0},
                        {'width': 2056, 'height': 1329, 'ratio': 2.0}
                    ],
                    'memory': [8, 16, 32, 64, 128],
                    'cores': [8, 10, 12, 16, 20]
                },
                'ubuntu_22': {
                    'os': 'X11; Linux x86_64',
                    'platform': 'Linux x86_64',
                    'resolutions': [
                        {'width': 1920, 'height': 1080, 'ratio': 1.0},
                        {'width': 1366, 'height': 768, 'ratio': 1.0},
                        {'width': 2560, 'height': 1440, 'ratio': 1.0},
                        {'width': 1600, 'height': 900, 'ratio': 1.0}
                    ],
                    'memory': [4, 8, 16, 32],
                    'cores': [2, 4, 6, 8, 12, 16]
                }
            },
            'mobile': {
                # iPhone Models
                'iphone_15_pro_max': {
                    'os': 'iPhone; CPU iPhone OS 17_1 like Mac OS X',
                    'platform': 'iPhone',
                    'resolutions': [{'width': 430, 'height': 932, 'ratio': 3.0}],
                    'memory': [8],
                    'cores': [6]
                },
                'iphone_15_pro': {
                    'os': 'iPhone; CPU iPhone OS 17_1 like Mac OS X',
                    'platform': 'iPhone',
                    'resolutions': [{'width': 393, 'height': 852, 'ratio': 3.0}],
                    'memory': [8],
                    'cores': [6]
                },
                'iphone_15_plus': {
                    'os': 'iPhone; CPU iPhone OS 17_0 like Mac OS X',
                    'platform': 'iPhone',
                    'resolutions': [{'width': 428, 'height': 926, 'ratio': 3.0}],
                    'memory': [6],
                    'cores': [6]
                },
                'iphone_15': {
                    'os': 'iPhone; CPU iPhone OS 17_0 like Mac OS X',
                    'platform': 'iPhone',
                    'resolutions': [{'width': 393, 'height': 852, 'ratio': 3.0}],
                    'memory': [6],
                    'cores': [6]
                },
                'iphone_14_pro_max': {
                    'os': 'iPhone; CPU iPhone OS 16_6 like Mac OS X',
                    'platform': 'iPhone',
                    'resolutions': [{'width': 430, 'height': 932, 'ratio': 3.0}],
                    'memory': [6],
                    'cores': [6]
                },
                'iphone_14_pro': {
                    'os': 'iPhone; CPU iPhone OS 16_6 like Mac OS X',
                    'platform': 'iPhone',
                    'resolutions': [{'width': 393, 'height': 852, 'ratio': 3.0}],
                    'memory': [6],
                    'cores': [6]
                },
                'iphone_14_plus': {
                    'os': 'iPhone; CPU iPhone OS 16_5 like Mac OS X',
                    'platform': 'iPhone',
                    'resolutions': [{'width': 428, 'height': 926, 'ratio': 3.0}],
                    'memory': [6],
                    'cores': [6]
                },
                'iphone_14': {
                    'os': 'iPhone; CPU iPhone OS 16_5 like Mac OS X',
                    'platform': 'iPhone',
                    'resolutions': [{'width': 390, 'height': 844, 'ratio': 3.0}],
                    'memory': [6],
                    'cores': [6]
                },
                'iphone_13_pro_max': {
                    'os': 'iPhone; CPU iPhone OS 15_7 like Mac OS X',
                    'platform': 'iPhone',
                    'resolutions': [{'width': 428, 'height': 926, 'ratio': 3.0}],
                    'memory': [6],
                    'cores': [6]
                },
                'iphone_13_pro': {
                    'os': 'iPhone; CPU iPhone OS 15_7 like Mac OS X',
                    'platform': 'iPhone',
                    'resolutions': [{'width': 390, 'height': 844, 'ratio': 3.0}],
                    'memory': [6],
                    'cores': [6]
                },
                'iphone_13': {
                    'os': 'iPhone; CPU iPhone OS 15_6 like Mac OS X',
                    'platform': 'iPhone',
                    'resolutions': [{'width': 390, 'height': 844, 'ratio': 3.0}],
                    'memory': [4],
                    'cores': [6]
                },
                'iphone_12_pro_max': {
                    'os': 'iPhone; CPU iPhone OS 14_8 like Mac OS X',
                    'platform': 'iPhone',
                    'resolutions': [{'width': 428, 'height': 926, 'ratio': 3.0}],
                    'memory': [6],
                    'cores': [6]
                },
                'iphone_12': {
                    'os': 'iPhone; CPU iPhone OS 14_7 like Mac OS X',
                    'platform': 'iPhone',
                    'resolutions': [{'width': 390, 'height': 844, 'ratio': 3.0}],
                    'memory': [4],
                    'cores': [6]
                },

                # Samsung Galaxy S Series
                'samsung_s24_ultra': {
                    'os': 'Linux; Android 14; SM-S928B',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 915, 'ratio': 3.0}],
                    'memory': [12, 16],
                    'cores': [8]
                },
                'samsung_s24_plus': {
                    'os': 'Linux; Android 14; SM-S926B',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 384, 'height': 854, 'ratio': 3.0}],
                    'memory': [12],
                    'cores': [8]
                },
                'samsung_s24': {
                    'os': 'Linux; Android 14; SM-S921B',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 360, 'height': 780, 'ratio': 3.0}],
                    'memory': [8],
                    'cores': [8]
                },
                'samsung_s23_ultra': {
                    'os': 'Linux; Android 13; SM-S918B',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 915, 'ratio': 3.0}],
                    'memory': [8, 12],
                    'cores': [8]
                },
                'samsung_s23_plus': {
                    'os': 'Linux; Android 13; SM-S916B',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 384, 'height': 854, 'ratio': 3.0}],
                    'memory': [8],
                    'cores': [8]
                },
                'samsung_s23': {
                    'os': 'Linux; Android 13; SM-S911B',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 360, 'height': 780, 'ratio': 3.0}],
                    'memory': [8, 12],
                    'cores': [8]
                },
                'samsung_s22_ultra': {
                    'os': 'Linux; Android 12; SM-S908B',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 915, 'ratio': 3.0}],
                    'memory': [8, 12],
                    'cores': [8]
                },
                'samsung_s22': {
                    'os': 'Linux; Android 12; SM-S901B',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 360, 'height': 780, 'ratio': 3.0}],
                    'memory': [8],
                    'cores': [8]
                },
                'samsung_s21_ultra': {
                    'os': 'Linux; Android 11; SM-G998B',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 915, 'ratio': 3.0}],
                    'memory': [12, 16],
                    'cores': [8]
                },
                'samsung_s21': {
                    'os': 'Linux; Android 11; SM-G991B',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 360, 'height': 780, 'ratio': 3.0}],
                    'memory': [8],
                    'cores': [8]
                },

                # Samsung Galaxy Note Series
                'samsung_note20_ultra': {
                    'os': 'Linux; Android 10; SM-N986B',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 915, 'ratio': 3.0}],
                    'memory': [12],
                    'cores': [8]
                },

                # Samsung Galaxy A Series
                'samsung_a54': {
                    'os': 'Linux; Android 13; SM-A546B',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 360, 'height': 780, 'ratio': 3.0}],
                    'memory': [6, 8],
                    'cores': [8]
                },
                'samsung_a34': {
                    'os': 'Linux; Android 13; SM-A346B',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 360, 'height': 780, 'ratio': 3.0}],
                    'memory': [6, 8],
                    'cores': [8]
                },
                'samsung_a14': {
                    'os': 'Linux; Android 13; SM-A146B',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 360, 'height': 780, 'ratio': 2.0}],
                    'memory': [4, 6],
                    'cores': [8]
                },

                # Google Pixel Series
                'pixel_8_pro': {
                    'os': 'Linux; Android 14; Pixel 8 Pro',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 915, 'ratio': 2.625}],
                    'memory': [12],
                    'cores': [8]
                },
                'pixel_8': {
                    'os': 'Linux; Android 14; Pixel 8',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 915, 'ratio': 2.625}],
                    'memory': [8],
                    'cores': [8]
                },
                'pixel_7_pro': {
                    'os': 'Linux; Android 13; Pixel 7 Pro',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 915, 'ratio': 2.625}],
                    'memory': [12],
                    'cores': [8]
                },
                'pixel_7': {
                    'os': 'Linux; Android 13; Pixel 7',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 915, 'ratio': 2.625}],
                    'memory': [8],
                    'cores': [8]
                },
                'pixel_6_pro': {
                    'os': 'Linux; Android 12; Pixel 6 Pro',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 915, 'ratio': 2.625}],
                    'memory': [12],
                    'cores': [8]
                },
                'pixel_6': {
                    'os': 'Linux; Android 12; Pixel 6',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 915, 'ratio': 2.625}],
                    'memory': [8],
                    'cores': [8]
                },
                'pixel_5': {
                    'os': 'Linux; Android 11; Pixel 5',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 393, 'height': 851, 'ratio': 2.75}],
                    'memory': [8],
                    'cores': [8]
                },

                # OnePlus Series
                'oneplus_12': {
                    'os': 'Linux; Android 14; CPH2573',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 3.0}],
                    'memory': [12, 16, 24],
                    'cores': [8]
                },
                'oneplus_11': {
                    'os': 'Linux; Android 13; CPH2449',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 3.0}],
                    'memory': [8, 12, 16],
                    'cores': [8]
                },
                'oneplus_10_pro': {
                    'os': 'Linux; Android 12; NE2213',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 3.0}],
                    'memory': [8, 12],
                    'cores': [8]
                },
                'oneplus_9_pro': {
                    'os': 'Linux; Android 11; LE2123',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 3.0}],
                    'memory': [8, 12],
                    'cores': [8]
                },
                'oneplus_nord_3': {
                    'os': 'Linux; Android 13; CPH2493',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 2.75}],
                    'memory': [8, 16],
                    'cores': [8]
                },

                # Xiaomi Series
                'xiaomi_14_ultra': {
                    'os': 'Linux; Android 14; 2405CPX3DG',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 3.0}],
                    'memory': [12, 16],
                    'cores': [8]
                },
                'xiaomi_14': {
                    'os': 'Linux; Android 14; 2401FPN6DG',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 3.0}],
                    'memory': [8, 12],
                    'cores': [8]
                },
                'xiaomi_13_pro': {
                    'os': 'Linux; Android 13; 2210132C',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 3.0}],
                    'memory': [8, 12],
                    'cores': [8]
                },
                'xiaomi_13': {
                    'os': 'Linux; Android 13; 2211133C',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 3.0}],
                    'memory': [8, 12],
                    'cores': [8]
                },
                'redmi_note_13_pro': {
                    'os': 'Linux; Android 13; 23090RA98G',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 393, 'height': 873, 'ratio': 2.75}],
                    'memory': [8, 12],
                    'cores': [8]
                },
                'redmi_note_12_pro': {
                    'os': 'Linux; Android 12; 22101316G',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 393, 'height': 873, 'ratio': 2.75}],
                    'memory': [6, 8],
                    'cores': [8]
                },
                'poco_f5_pro': {
                    'os': 'Linux; Android 13; 23013PC75G',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 3.0}],
                    'memory': [8, 12],
                    'cores': [8]
                },

                # Oppo Series
                'oppo_find_x6_pro': {
                    'os': 'Linux; Android 13; PHB110',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 3.0}],
                    'memory': [12, 16],
                    'cores': [8]
                },
                'oppo_reno_10_pro': {
                    'os': 'Linux; Android 13; CPH2525',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 2.75}],
                    'memory': [12],
                    'cores': [8]
                },

                # Vivo Series
                'vivo_x100_pro': {
                    'os': 'Linux; Android 14; V2309A',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 3.0}],
                    'memory': [12, 16],
                    'cores': [8]
                },
                'vivo_v29_pro': {
                    'os': 'Linux; Android 13; V2250',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 2.75}],
                    'memory': [8, 12],
                    'cores': [8]
                },

                # Realme Series
                'realme_gt5_pro': {
                    'os': 'Linux; Android 14; RMX3708',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 3.0}],
                    'memory': [12, 16],
                    'cores': [8]
                },
                'realme_11_pro_plus': {
                    'os': 'Linux; Android 13; RMX3741',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 2.75}],
                    'memory': [8, 12],
                    'cores': [8]
                },

                # Huawei Series
                'huawei_p60_pro': {
                    'os': 'Linux; Android 13; ALN-L29',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 3.0}],
                    'memory': [8, 12],
                    'cores': [8]
                },
                'huawei_mate_50_pro': {
                    'os': 'Linux; Android 12; DCO-L29',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 3.0}],
                    'memory': [8],
                    'cores': [8]
                },

                # Honor Series
                'honor_90_pro': {
                    'os': 'Linux; Android 13; REA-AN00',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 2.75}],
                    'memory': [12, 16],
                    'cores': [8]
                },

                # Nothing Series
                'nothing_phone_2': {
                    'os': 'Linux; Android 13; A065',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 2.75}],
                    'memory': [8, 12],
                    'cores': [8]
                },

                # Motorola Series
                'motorola_edge_40_pro': {
                    'os': 'Linux; Android 13; XT2301-4',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 412, 'height': 919, 'ratio': 2.75}],
                    'memory': [8, 12],
                    'cores': [8]
                },

                # Sony Series
                'sony_xperia_1_v': {
                    'os': 'Linux; Android 13; XQ-DQ72',
                    'platform': 'Linux armv8l',
                    'resolutions': [{'width': 384, 'height': 854, 'ratio': 3.5}],
                    'memory': [12],
                    'cores': [8]
                },
            },
            'tablet': {
                'ipad_pro_12': {
                    'os': 'OS 16_6 like Mac OS X',
                    'platform': 'iPad',
                    'resolutions': [{'width': 1024, 'height': 1366, 'ratio': 2.0}],
                    'memory': [8, 16],
                    'cores': [8]
                },
                'surface_pro_9': {
                    'os': 'Windows NT 10.0; Win64; x64',
                    'platform': 'Win32',
                    'resolutions': [{'width': 1368, 'height': 912, 'ratio': 1.5}],
                    'memory': [8, 16, 32],
                    'cores': [4, 8, 12]
                }
            }
        }

    def _get_latest_browser_versions(self):
        """Latest browser versions get karte hain"""
        return {
            'chrome': {
                'stable': ['120.0.6099.109', '120.0.6099.110', '120.0.6099.129', '121.0.6167.85', '121.0.6167.139'],
                'beta': ['121.0.6167.85', '122.0.6261.29'],
                'dev': ['122.0.6261.29', '123.0.6312.4']
            },
            'firefox': {
                'stable': ['121.0', '121.0.1', '122.0', '122.0.1'],
                'beta': ['122.0b9', '123.0b1'],
                'nightly': ['123.0a1']
            },
            'safari': {
                'stable': ['17.2.1', '17.3', '17.3.1'],
                'technology_preview': ['17.4']
            },
            'edge': {
                'stable': ['120.0.2210.133', '121.0.2277.83', '121.0.2277.98'],
                'beta': ['122.0.2365.8'],
                'dev': ['123.0.2420.5']
            }
        }

    def generate_user_agent(self, device_type='desktop', browser='chrome'):
        """Advanced user agent generate karte hain"""
        device_profile = random.choice(list(self.device_profiles[device_type].values()))

        if browser == 'chrome':
            version = random.choice(self.browser_versions['chrome']['stable'])
            webkit_version = f"537.{random.randint(30, 40)}"

            if 'iPhone' in device_profile['os']:
                return f"Mozilla/5.0 ({device_profile['os']}) AppleWebKit/{webkit_version} (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/{webkit_version}"
            elif 'Android' in device_profile['os']:
                return f"Mozilla/5.0 (Linux; Android {random.randint(10, 13)}; {device_profile['os'].split(';')[-1].strip()}) AppleWebKit/{webkit_version} (KHTML, like Gecko) Chrome/{version} Mobile Safari/{webkit_version}"
            else:
                return f"Mozilla/5.0 ({device_profile['os']}) AppleWebKit/{webkit_version} (KHTML, like Gecko) Chrome/{version} Safari/{webkit_version}"

        elif browser == 'firefox':
            version = random.choice(self.browser_versions['firefox']['stable'])
            gecko_version = f"{random.randint(20100101, 20231231)}"

            if 'iPhone' in device_profile['os']:
                return f"Mozilla/5.0 ({device_profile['os']}) Gecko/{gecko_version} Firefox/{version}"
            elif 'Android' in device_profile['os']:
                return f"Mozilla/5.0 (Mobile; rv:{version}) Gecko/{version} Firefox/{version}"
            else:
                return f"Mozilla/5.0 ({device_profile['os']}; rv:{version}) Gecko/{gecko_version} Firefox/{version}"

        elif browser == 'safari':
            version = random.choice(self.browser_versions['safari']['stable'])
            webkit_version = f"605.1.{random.randint(10, 20)}"

            if 'iPhone' in device_profile['os']:
                return f"Mozilla/5.0 ({device_profile['os']}) AppleWebKit/{webkit_version} (KHTML, like Gecko) Version/{version} Mobile/15E148 Safari/{webkit_version}"
            elif 'Mac' in device_profile['os']:
                return f"Mozilla/5.0 ({device_profile['os']}) AppleWebKit/{webkit_version} (KHTML, like Gecko) Version/{version} Safari/{webkit_version}"

        return self.generate_user_agent(device_type, 'chrome')  # fallback

    def get_device_profile(self, device_type='random'):
        """Device profile get karte hain"""
        if device_type == 'random':
            device_type = random.choice(['desktop', 'mobile', 'tablet'])

        device_profiles = self.device_profiles[device_type]
        device_name = random.choice(list(device_profiles.keys()))
        profile = device_profiles[device_name]

        resolution = random.choice(profile['resolutions'])
        memory = random.choice(profile['memory'])
        cores = random.choice(profile['cores'])

        return {
            'type': device_type,
            'name': device_name,
            'os': profile['os'],
            'platform': profile['platform'],
            'resolution': resolution,
            'memory': memory,
            'cores': cores
        }

    def generate_canvas_fingerprint(self):
        """Canvas fingerprint generate karte hain"""
        canvas_data = {
            'text_rendering': random.choice(['subpixel', 'optimizeSpeed', 'optimizeQuality', 'geometricPrecision']),
            'font_smoothing': random.choice(['auto', 'never', 'always']),
            'webgl_vendor': random.choice(['Google Inc.', 'Mozilla', 'Apple Inc.', 'Microsoft Corporation']),
            'webgl_renderer': random.choice([
                'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                'ANGLE (AMD, AMD Radeon RX 580 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                'Apple GPU',
                'Mali-G78 MP14'
            ])
        }
        return canvas_data

    def generate_audio_fingerprint(self):
        """Audio fingerprint generate karte hain"""
        return {
            'sample_rate': random.choice([44100, 48000, 96000]),
            'buffer_size': random.choice([128, 256, 512, 1024]),
            'channels': random.choice([1, 2, 6, 8]),
            'bit_depth': random.choice([16, 24, 32])
        }

    def generate_webrtc_fingerprint(self):
        """WebRTC fingerprint generate karte hain"""
        return {
            'local_ip': f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            'public_ip': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            'ice_candidates': random.randint(2, 8),
            'dtls_fingerprint': hashlib.sha256(str(random.random()).encode()).hexdigest()[:32]
        }

    def generate_timezone_data(self):
        """Timezone data generate karte hain"""
        timezones = [
            {'id': 'America/New_York', 'offset': -5, 'dst': True},
            {'id': 'America/Los_Angeles', 'offset': -8, 'dst': True},
            {'id': 'Europe/London', 'offset': 0, 'dst': True},
            {'id': 'Europe/Berlin', 'offset': 1, 'dst': True},
            {'id': 'Asia/Tokyo', 'offset': 9, 'dst': False},
            {'id': 'Asia/Shanghai', 'offset': 8, 'dst': False},
            {'id': 'Asia/Kolkata', 'offset': 5.5, 'dst': False},
            {'id': 'Australia/Sydney', 'offset': 11, 'dst': True},
            {'id': 'America/Chicago', 'offset': -6, 'dst': True},
            {'id': 'Europe/Paris', 'offset': 1, 'dst': True},
            {'id': 'Asia/Dubai', 'offset': 4, 'dst': False},
            {'id': 'America/Toronto', 'offset': -5, 'dst': True}
        ]
        return random.choice(timezones)

    def generate_language_settings(self):
        """Language settings generate karte hain"""
        languages = [
            {'primary': 'en-US', 'accept': 'en-US,en;q=0.9'},
            {'primary': 'en-GB', 'accept': 'en-GB,en;q=0.9'},
            {'primary': 'en-IN', 'accept': 'en-IN,en;q=0.9,hi;q=0.8'},
            {'primary': 'es-ES', 'accept': 'es-ES,es;q=0.9,en;q=0.8'},
            {'primary': 'fr-FR', 'accept': 'fr-FR,fr;q=0.9,en;q=0.8'},
            {'primary': 'de-DE', 'accept': 'de-DE,de;q=0.9,en;q=0.8'},
            {'primary': 'ja-JP', 'accept': 'ja-JP,ja;q=0.9,en;q=0.8'},
            {'primary': 'zh-CN', 'accept': 'zh-CN,zh;q=0.9,en;q=0.8'},
            {'primary': 'pt-BR', 'accept': 'pt-BR,pt;q=0.9,en;q=0.8'},
            {'primary': 'ru-RU', 'accept': 'ru-RU,ru;q=0.9,en;q=0.8'}
        ]
        return random.choice(languages)

    def generate_hardware_fingerprint(self, device_profile):
        """Hardware fingerprint generate karte hain"""
        return {
            'cpu_cores': device_profile['cores'],
            'memory_gb': device_profile['memory'],
            'gpu_vendor': random.choice(['NVIDIA', 'AMD', 'Intel', 'Apple', 'Mali', 'Adreno']),
            'storage_type': random.choice(['SSD', 'HDD', 'NVMe', 'eMMC']),
            'battery_level': random.randint(20, 100) if device_profile['type'] in ['mobile', 'tablet'] else None,
            'charging': random.choice([True, False]) if device_profile['type'] in ['mobile', 'tablet'] else None
        }

    def generate_network_fingerprint(self):
        """Network fingerprint generate karte hain"""
        connection_types = ['wifi', 'ethernet', 'cellular', '5g', '4g', '3g']
        if random.choice([True, False]):  # Mobile device
            connection = random.choice(['wifi', 'cellular', '5g', '4g'])
        else:  # Desktop
            connection = random.choice(['wifi', 'ethernet'])

        return {
            'connection_type': connection,
            'downlink': random.uniform(1.0, 100.0),
            'rtt': random.randint(10, 200),
            'effective_type': random.choice(['slow-2g', '2g', '3g', '4g']),
            'save_data': random.choice([True, False])
        }

    def generate_browser_plugins(self, device_profile):
        """Browser plugins generate karte hain"""
        common_plugins = [
            'Chrome PDF Plugin',
            'Chrome PDF Viewer',
            'Native Client',
            'Widevine Content Decryption Module'
        ]

        if device_profile['type'] == 'desktop':
            desktop_plugins = [
                'Adobe Flash Player',
                'Java Deployment Toolkit',
                'Microsoft Silverlight',
                'VLC Web Plugin',
                'QuickTime Plug-in'
            ]
            plugins = common_plugins + random.sample(desktop_plugins, random.randint(0, 3))
        else:
            plugins = common_plugins

        return plugins

    def generate_fonts_list(self, device_profile):
        """Fonts list generate karte hain"""
        common_fonts = [
            'Arial', 'Helvetica', 'Times New Roman', 'Courier New', 'Verdana',
            'Georgia', 'Palatino', 'Garamond', 'Bookman', 'Comic Sans MS',
            'Trebuchet MS', 'Arial Black', 'Impact'
        ]

        if 'Windows' in device_profile['os']:
            windows_fonts = [
                'Segoe UI', 'Calibri', 'Cambria', 'Consolas', 'Corbel',
                'Franklin Gothic Medium', 'Lucida Console', 'Lucida Sans Unicode',
                'Microsoft Sans Serif', 'Tahoma'
            ]
            fonts = common_fonts + windows_fonts
        elif 'Mac' in device_profile['os'] or 'iPhone' in device_profile['os']:
            mac_fonts = [
                'San Francisco', 'Helvetica Neue', 'Lucida Grande', 'Monaco',
                'Menlo', 'Avenir', 'Optima', 'Futura', 'Gill Sans'
            ]
            fonts = common_fonts + mac_fonts
        else:  # Linux/Android
            linux_fonts = [
                'Ubuntu', 'Liberation Sans', 'DejaVu Sans', 'Noto Sans',
                'Roboto', 'Droid Sans', 'Open Sans'
            ]
            fonts = common_fonts + linux_fonts

        return random.sample(fonts, random.randint(15, len(fonts)))

    def generate_random_email(self):
        """Random email generate karte hain"""
        domains = [
            'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'protonmail.com',
            'mail.com', 'icloud.com', 'aol.com', 'zoho.com', 'yandex.com',
            'tutanota.com', 'fastmail.com', 'gmx.com', 'live.com', 'msn.com'
        ]

        prefixes = ['user', 'test', 'demo', 'sample', 'temp', 'new', 'my', 'the']
        suffixes = ['123', '456', '789', '2024', '2023', 'x', 'pro', 'dev']

        if random.choice([True, False]):
            # Simple username
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(6, 12)))
        else:
            # Prefix + random + suffix
            prefix = random.choice(prefixes)
            middle = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 8)))
            suffix = random.choice(suffixes)
            username = f"{prefix}{middle}{suffix}"

        return f"{username}@{random.choice(domains)}"

    def generate_complete_fingerprint(self, device_type='random', browser='chrome'):
        """Complete fingerprint generate karte hain"""
        device_profile = self.get_device_profile(device_type)
        user_agent = self.generate_user_agent(device_profile['type'], browser)
        timezone_data = self.generate_timezone_data()
        language_data = self.generate_language_settings()
        canvas_fp = self.generate_canvas_fingerprint()
        audio_fp = self.generate_audio_fingerprint()
        webrtc_fp = self.generate_webrtc_fingerprint()
        hardware_fp = self.generate_hardware_fingerprint(device_profile)
        network_fp = self.generate_network_fingerprint()
        plugins = self.generate_browser_plugins(device_profile)
        fonts = self.generate_fonts_list(device_profile)

        return {
            'device': device_profile,
            'user_agent': user_agent,
            'timezone': timezone_data,
            'language': language_data,
            'canvas': canvas_fp,
            'audio': audio_fp,
            'webrtc': webrtc_fp,
            'hardware': hardware_fp,
            'network': network_fp,
            'plugins': plugins,
            'fonts': fonts,
            'session_id': str(uuid.uuid4()),
            'generated_at': datetime.now().isoformat()
        }

    def solve_captcha(self, page, captcha_type='image'):
        """
        CAPTCHA solve karne ka attempt karta hai
        :param page: Playwright page object
        :param captcha_type: 'image', 'text', or 'recaptcha'
        :return: True if CAPTCHA solved, False otherwise
        """
        attempts = 0
        solved = False

        while attempts < self.captcha_config['max_attempts'] and not solved:
            attempts += 1
            print(f"🔄 CAPTCHA solve karne ka attempt {attempts}/{self.captcha_config['max_attempts']}")

            try:
                if captcha_type == 'image':
                    # Image CAPTCHA handling
                    captcha_element = page.query_selector('img[src*="captcha"], img[alt*="CAPTCHA"], img[alt*="captcha"], img[id*="captcha"], img[class*="captcha"]')
                    if captcha_element:
                        # Get the CAPTCHA image
                        captcha_src = captcha_element.get_attribute('src')

                        if captcha_src and captcha_src.startswith('data:image'):
                            # Handle base64 encoded image
                            image_data = captcha_src.split(',')[1]
                            image = Image.open(io.BytesIO(base64.b64decode(image_data)))
                        elif captcha_src:
                            # Handle URL-based image (would require download)
                            print("⚠️ URL-based CAPTCHA images require additional handling")
                            if self.captcha_config['manual_fallback']:
                                print("ℹ️ Manual CAPTCHA solving required - browser open hai")
                                input("👉 CAPTCHA solve karke Enter dabayein...")
                                return True
                            return False
                        else:
                            print("❌ CAPTCHA image source nahi mila")
                            continue

                        if self.captcha_config['ocr_enabled']:
                            try:
                                # Use OCR to solve CAPTCHA
                                captcha_text = pytesseract.image_to_string(image, config='--psm 8 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz').strip()
                                if captcha_text:
                                    # Find the input field and enter the text
                                    captcha_input = page.query_selector('input[name*="captcha"], input[id*="captcha"], input[placeholder*="captcha"], input[class*="captcha"]')
                                    if captcha_input:
                                        captcha_input.fill(captcha_text)
                                        print(f"📝 OCR se CAPTCHA solution: {captcha_text}")

                                        # Find and click submit button
                                        submit_button = page.query_selector('button[type="submit"], input[type="submit"], button:has-text("Submit"), button:has-text("Verify")')
                                        if submit_button:
                                            submit_button.click()
                                            page.wait_for_timeout(2000)  # Wait for possible page change

                                            # Check if CAPTCHA was successful
                                            if not page.query_selector('img[src*="captcha"], img[alt*="CAPTCHA"]'):
                                                solved = True
                                                print("✅ CAPTCHA successfully solve ho gaya!")
                                        else:
                                            print("⚠️ Submit button nahi mila")
                                    else:
                                        print("⚠️ CAPTCHA input field nahi mila")
                                else:
                                    print("⚠️ OCR se text extract nahi hua")
                            except Exception as e:
                                print(f"❌ OCR error: {str(e)}")

                elif captcha_type == 'recaptcha':
                    # reCAPTCHA handling
                    recaptcha_frame = page.query_selector('iframe[src*="recaptcha"]')
                    if recaptcha_frame:
                        print("🔍 reCAPTCHA detect hua hai")

                        if self.captcha_config['manual_fallback']:
                            print("ℹ️ Manual reCAPTCHA solving required - browser open hai")
                            input("👉 reCAPTCHA solve karke Enter dabayein...")
                            return True

                # Wait before next attempt
                if not solved:
                    page.wait_for_timeout(self.captcha_config['wait_time'] * 1000)

            except Exception as e:
                print(f"❌ CAPTCHA solve karne mein error: {str(e)}")
                page.wait_for_timeout(self.captcha_config['wait_time'] * 1000)

        return solved

    def handle_captcha_challenge(self, page):
        """
        Various types ke CAPTCHA challenges handle karta hai
        :param page: Playwright page object
        :return: True if CAPTCHA handled, False otherwise
        """
        # Check for different types of CAPTCHAs
        captcha_detected = False

        print("🔍 Page par CAPTCHA check kar rahe hain...")

        # 1. Image CAPTCHA
        captcha_img = page.query_selector('img[src*="captcha"], img[alt*="CAPTCHA"], img[alt*="captcha"], img[id*="captcha"], img[class*="captcha"]')
        if captcha_img:
            print("📷 Image CAPTCHA detect hua hai")
            return self.solve_captcha(page, 'image')

        # 2. reCAPTCHA
        recaptcha = page.query_selector('iframe[src*="recaptcha"], .g-recaptcha, [data-sitekey]')
        if recaptcha:
            print("🛡️ reCAPTCHA detect hua hai")
            return self.solve_captcha(page, 'recaptcha')

        # 3. Text-based CAPTCHA
        captcha_input = page.query_selector('input[name*="captcha"], input[id*="captcha"], input[placeholder*="captcha"], input[class*="captcha"]')
        if captcha_input:
            print("🔤 Text CAPTCHA detect hua hai")
            if self.captcha_config['manual_fallback']:
                print("ℹ️ Manual CAPTCHA solving required - browser open hai")
                input("👉 CAPTCHA solve karke Enter dabayein...")
                return True

        # 4. hCaptcha
        hcaptcha = page.query_selector('iframe[src*="hcaptcha"], .h-captcha, [data-hcaptcha-sitekey]')
        if hcaptcha:
            print("🔒 hCaptcha detect hua hai")
            if self.captcha_config['manual_fallback']:
                print("ℹ️ Manual hCaptcha solving required - browser open hai")
                input("👉 hCaptcha solve karke Enter dabayein...")
                return True

        # 5. Cloudflare CAPTCHA
        cloudflare = page.query_selector('[data-ray], .cf-browser-verification, .cf-challenge-running, .cf-im-under-attack')
        if cloudflare:
            print("☁️ Cloudflare CAPTCHA detect hua hai")
            if self.captcha_config['manual_fallback']:
                print("ℹ️ Manual Cloudflare CAPTCHA solving required - browser open hai")
                input("👉 Cloudflare CAPTCHA solve karke Enter dabayein...")
                return True

        # 6. Generic CAPTCHA detection
        generic_captcha = page.query_selector('[class*="captcha"], [id*="captcha"], [name*="captcha"]')
        if generic_captcha:
            print("🎯 Generic CAPTCHA element detect hua hai")
            print(f"Element: {generic_captcha.get_attribute('outerHTML')[:100]}...")
            if self.captcha_config['manual_fallback']:
                print("ℹ️ Manual CAPTCHA solving required - browser open hai")
                input("👉 CAPTCHA solve karke Enter dabayein...")
                return True

        print("✅ Koi CAPTCHA detect nahi hua - page clear hai")
        return False

    def handle_auth0_redirects(self, page, target_url):
        """
        Handle Auth0 authentication redirects
        """
        print("🔐 Auth0 login page detect hua hai")

        # Wait for Auth0 page to fully load
        try:
            page.wait_for_selector('input[type="email"], input[name="username"], input[id="username"]', timeout=10000)
            print("✅ Auth0 login form load ho gaya")

            # Check if we're on the correct login page
            current_url = page.url
            if "login.augmentcode.com" in current_url or "auth0.com" in current_url:
                print(f"🎯 Auth0 login page: {current_url}")
                return True
            else:
                print(f"⚠️ Unexpected redirect: {current_url}")
                return False

        except Exception as e:
            print(f"⚠️ Auth0 page load issue: {str(e)}")
            return False

    def navigate_with_captcha_handling(self, page, url, max_retries=3):
        """
        Page navigation with CAPTCHA handling and Auth0 support
        """
        retries = 0

        # Check if this is an Auth0 login URL
        is_auth0_url = "login.augmentcode.com" in url or "auth0.com" in url

        while retries < max_retries:
            try:
                print(f"🌐 {url} par navigate kar rahe hain...")

                # Special handling for Auth0 URLs
                if is_auth0_url:
                    # For Auth0, use wait_until: 'domcontentloaded' instead of 'load'
                    page.goto(url, wait_until='domcontentloaded', timeout=30000)

                    # Wait for Auth0 specific elements
                    try:
                        page.wait_for_selector('body', timeout=10000)
                        print("✅ Auth0 page body load ho gaya")

                        # Check if we got redirected to home page
                        current_url = page.url
                        if "login.augmentcode.com" not in current_url and "auth0.com" not in current_url:
                            if "augmentcode.com" in current_url:
                                print("⚠️ Auth0 redirect ho gaya home page par")
                                print(f"🔗 Current URL: {current_url}")
                                print("💡 Manually login page par jane ke liye browser use kariye")
                            else:
                                print(f"🔗 Redirected to: {current_url}")
                        else:
                            print("✅ Auth0 login page successfully load ho gaya")

                    except Exception as auth_error:
                        print(f"⚠️ Auth0 loading issue: {str(auth_error)}")

                else:
                    # Regular navigation for non-Auth0 URLs
                    page.goto(url, timeout=30000)

                    # Try different wait strategies
                    try:
                        # First try networkidle with shorter timeout
                        page.wait_for_load_state('networkidle', timeout=5000)
                        print("✅ Page networkidle state mein load ho gaya")
                    except:
                        try:
                            # If networkidle fails, try domcontentloaded
                            page.wait_for_load_state('domcontentloaded', timeout=5000)
                            print("✅ Page DOM content load ho gaya")
                        except:
                            # If both fail, just wait for basic load
                            page.wait_for_load_state('load', timeout=5000)
                            print("✅ Page basic load ho gaya")

                # Check for CAPTCHA immediately after navigation
                if self.handle_captcha_challenge(page):
                    print("✅ CAPTCHA solve karne ke baad page load ho gaya")
                    return True

                # Check if page loaded successfully
                if page.url and not page.url.startswith('about:blank'):
                    print("✅ Page successfully load ho gaya")
                    return True

            except Exception as e:
                retries += 1
                print(f"❌ Navigation error (Attempt {retries}/{max_retries}): {str(e)}")
                if retries < max_retries:
                    print(f"⏳ {self.captcha_config['wait_time']} seconds wait kar rahe hain...")
                    page.wait_for_timeout(self.captcha_config['wait_time'] * 1000)  # Wait before retry

        # Even if navigation "failed", check if page is actually accessible
        try:
            if page.url and not page.url.startswith('about:blank'):
                print("⚠️ Navigation timeout hua lekin page accessible hai")
                # Still check for CAPTCHA
                self.handle_captcha_challenge(page)
                return True
        except:
            pass

        print("❌ Maximum retries reach ho gaye, navigation fail ho gaya")
        return False

def run_advanced_browser(device_type='random', browser_type='chrome', show_details=True, target_url=None):
    """Advanced browser fingerprinting ke saath browser run karte hain"""
    fingerprinter = AdvancedFingerprinter()

    # Complete fingerprint generate karte hain
    fingerprint = fingerprinter.generate_complete_fingerprint(device_type, browser_type)

    with sync_playwright() as p:
        # Browser launch arguments - Enhanced for Auth0 and login pages
        launch_args = [
            f'--user-agent={fingerprint["user_agent"]}',
            f'--window-size={fingerprint["device"]["resolution"]["width"]},{fingerprint["device"]["resolution"]["height"]}',
            '--disable-blink-features=AutomationControlled',
            '--disable-infobars',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-extensions',
            '--disable-popup-blocking',
            f'--lang={fingerprint["language"]["primary"].split("-")[0]}',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-features=TranslateUI',
            '--disable-ipc-flooding-protection',
            '--disable-features=VizDisplayCompositor',
            '--disable-default-apps',
            '--disable-sync',
            '--no-first-run',
            '--disable-component-update'
        ]

        # Browser launch karte hain
        browser = p.chromium.launch(
            headless=False,
            args=launch_args
        )

        # Context create karte hain with advanced settings for Auth0 compatibility
        context = browser.new_context(
            user_agent=fingerprint["user_agent"],
            viewport={
                'width': fingerprint["device"]["resolution"]["width"],
                'height': fingerprint["device"]["resolution"]["height"]
            },
            locale=fingerprint["language"]["primary"],
            timezone_id=fingerprint["timezone"]["id"],
            permissions=['geolocation', 'notifications'],
            color_scheme=random.choice(['light', 'dark']),
            device_scale_factor=fingerprint["device"]["resolution"]["ratio"],
            extra_http_headers={
                'Accept-Language': fingerprint["language"]["accept"],
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cache-Control': 'max-age=0',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Upgrade-Insecure-Requests': '1'
            },
            # Enable JavaScript and cookies for Auth0
            java_script_enabled=True,
            accept_downloads=True,
            ignore_https_errors=True
        )

        # Page create karte hain
        page = context.new_page()

        # Advanced fingerprint injection
        page.add_init_script(f"""
            // Hardware concurrency override
            Object.defineProperty(navigator, 'hardwareConcurrency', {{
                get: () => {fingerprint["hardware"]["cpu_cores"]}
            }});

            // Memory override
            Object.defineProperty(navigator, 'deviceMemory', {{
                get: () => {fingerprint["hardware"]["memory_gb"]}
            }});

            // Platform override
            Object.defineProperty(navigator, 'platform', {{
                get: () => '{fingerprint["device"]["platform"]}'
            }});

            // WebGL fingerprint override
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) {{
                    return '{fingerprint["canvas"]["webgl_vendor"]}';
                }}
                if (parameter === 37446) {{
                    return '{fingerprint["canvas"]["webgl_renderer"]}';
                }}
                return getParameter.call(this, parameter);
            }};

            // Screen resolution override
            Object.defineProperty(screen, 'width', {{
                get: () => {fingerprint["device"]["resolution"]["width"]}
            }});
            Object.defineProperty(screen, 'height', {{
                get: () => {fingerprint["device"]["resolution"]["height"]}
            }});

            // Remove automation indicators
            delete navigator.__proto__.webdriver;
            Object.defineProperty(navigator, 'webdriver', {{
                get: () => undefined
            }});
        """)

        try:
            target_url = target_url or 'https://www.augmentcode.com/'
            print(f"🚀 {target_url} website par ja rahe hain...")

            navigation_success = fingerprinter.navigate_with_captcha_handling(page, target_url)

            if not navigation_success:
                print("⚠️ Navigation timeout hua, lekin browser manually use kar sakte hain")

            # Always check for CAPTCHA regardless of navigation status
            fingerprinter.handle_captcha_challenge(page)

            # Try to get page info
            try:
                page_title = page.title()
                current_url = page.url
                print(f"📄 Current page: {page_title}")
                print(f"🔗 Current URL: {current_url}")

                if target_url == 'https://www.augmentcode.com/' and "augment" in page_title.lower():
                    print("✅ Augment website successfully load ho gayi!")
                elif current_url and not current_url.startswith('about:blank'):
                    print("✅ Website accessible hai!")
                else:
                    print("⚠️ Website status unclear, manually check kariye")

            except Exception as page_error:
                print(f"⚠️ Page info get nahi kar paye: {str(page_error)}")
                print("💡 Browser manually use kar sakte hain")

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("💡 Browser open hai, manually use kar sakte hain")

        if show_details:
            print("\n" + "="*60)
            print("🔍 ADVANCED BROWSER FINGERPRINT DETAILS")
            print("="*60)
            print(f"📱 Device Type: {fingerprint['device']['type'].title()}")
            print(f"🏷️  Device Name: {fingerprint['device']['name'].replace('_', ' ').title()}")
            print(f"💻 OS: {fingerprint['device']['os']}")
            print(f"🌐 User Agent: {fingerprint['user_agent'][:80]}...")
            print(f"📺 Resolution: {fingerprint['device']['resolution']['width']}x{fingerprint['device']['resolution']['height']} (Ratio: {fingerprint['device']['resolution']['ratio']})")
            print(f"🧠 Memory: {fingerprint['hardware']['memory_gb']}GB")
            print(f"⚙️  CPU Cores: {fingerprint['hardware']['cpu_cores']}")
            print(f"🎨 GPU: {fingerprint['canvas']['webgl_renderer']}")
            print(f"🌍 Timezone: {fingerprint['timezone']['id']}")
            print(f"🗣️  Language: {fingerprint['language']['primary']}")
            print(f"📶 Network: {fingerprint['network']['connection_type'].title()}")
            print(f"🔌 Plugins: {len(fingerprint['plugins'])} installed")
            print(f"🔤 Fonts: {len(fingerprint['fonts'])} available")
            print(f"🆔 Session ID: {fingerprint['session_id']}")
            print("="*60)

        print("\n🎯 Ab aap manually ye kar sakte hain:")
        print("1. 📝 Signup page par ja sakte hain")
        print("2. 🆕 Naya account bana sakte hain")
        print("3. 🔧 Extension ka use kar sakte hain")
        print("4. 🧪 Different websites test kar sakte hain\n")

        input("⏹️  Browser band karne ke liye Enter dabayein...")
        browser.close()

        return fingerprint

def run_multiple_browsers(count=3, device_types=['desktop', 'mobile', 'tablet']):
    """Multiple browsers with different fingerprints run karte hain"""
    print(f"🚀 {count} different browsers launch kar rahe hain...\n")

    for i in range(count):
        device_type = random.choice(device_types)
        browser_type = random.choice(['chrome', 'firefox', 'safari'])

        print(f"🌟 Browser {i+1}/{count} - {device_type.title()} ({browser_type.title()})")
        fingerprint = run_advanced_browser(device_type, browser_type, show_details=False)

        print(f"✅ Browser {i+1} ready hai!")
        if i < count - 1:
            input("⏭️  Next browser ke liye Enter dabayein...")
            print()

def show_device_options():
    """Available device options show karte hain"""
    fingerprinter = AdvancedFingerprinter()

    print("\n" + "="*50)
    print("📱 AVAILABLE DEVICE OPTIONS")
    print("="*50)

    for category, devices in fingerprinter.device_profiles.items():
        print(f"\n🔸 {category.upper()}:")
        for device_name in devices.keys():
            device_display = device_name.replace('_', ' ').title()
            print(f"   • {device_display}")

    print("\n" + "="*50)

if __name__ == "__main__":
    print("🎭 ADVANCED BROWSER FINGERPRINTING TOOL WITH CAPTCHA HANDLING")
    print("="*60)

    while True:
        print("\n🎯 Options:")
        print("1. 🚀 Single browser launch karo (random device)")
        print("2. 📱 Specific device type choose karo")
        print("3. 🔄 Multiple browsers launch karo")
        print("4. 📋 Available devices dekho")
        print("5. 🌐 Custom website test karo")
        print("6. ❌ Exit")

        choice = input("\n👉 Apna choice enter karo (1-6): ").strip()

        if choice == '1':
            run_advanced_browser()
        elif choice == '2':
            show_device_options()
            device_type = input("\n👉 Device type enter karo (desktop/mobile/tablet): ").strip().lower()
            if device_type in ['desktop', 'mobile', 'tablet']:
                browser_type = input("👉 Browser type enter karo (chrome/firefox/safari): ").strip().lower()
                if browser_type in ['chrome', 'firefox', 'safari']:
                    run_advanced_browser(device_type, browser_type)
                else:
                    run_advanced_browser(device_type)
            else:
                print("❌ Invalid device type!")
        elif choice == '3':
            try:
                count = int(input("👉 Kitne browsers launch karne hain? (1-10): "))
                if 1 <= count <= 10:
                    run_multiple_browsers(count)
                else:
                    print("❌ 1-10 ke beech number enter karo!")
            except ValueError:
                print("❌ Valid number enter karo!")
        elif choice == '4':
            show_device_options()
        elif choice == '5':
            target_url = input("👉 Website URL enter karo (e.g., https://example.com): ").strip()
            if target_url.startswith('http'):
                run_advanced_browser(target_url=target_url)
            else:
                print("❌ Valid URL enter karo (https:// ke saath)")
        elif choice == '6':
            print("👋 Bye! Happy browsing!")
            break
        else:
            print("❌ Invalid choice! 1-6 ke beech select karo.")