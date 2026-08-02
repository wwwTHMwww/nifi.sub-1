import re
import hashlib
from typing import List, Set
from .config import MAX_CONFIGS, MIN_LENGTH

def extract_configs(text: str) -> List[str]:
    """استخراج کانفیگ‌ها از متن"""
    configs = []
    
    # الگوهای کانفیگ
    patterns = [
        r'vmess://[a-zA-Z0-9+/=_-]+',
        r'vless://[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+:\d+[^\s]+',
        r'trojan://[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+:\d+[^\s]+',
        r'ss://[a-zA-Z0-9+/=_-]+@[a-zA-Z0-9.-]+:\d+[^\s]+',
        r'ssr://[a-zA-Z0-9+/=_-]+',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        configs.extend(matches)
    
    return configs

def clean_config(config: str) -> str:
    """پاک‌سازی کانفیگ"""
    # حذف whitespace اضافی
    config = config.strip()
    
    # حذف تگ‌های اضافی
    config = re.sub(r'#[^\s]+', '', config)
    
    return config

def is_valid(config: str) -> bool:
    """اعتبارسنجی کانفیگ"""
    if len(config) < MIN_LENGTH:
        return False
    
    # بررسی پروتکل معتبر
    valid_protocols = ['vmess://', 'vless://', 'trojan://', 'ss://', 'ssr://']
    if not any(config.startswith(p) for p in valid_protocols):
        return False
    
    return True

def get_hash(config: str) -> str:
    """تولید هش برای حذف تکراری"""
    # حذف بخش‌های متغیر برای تشخیص بهتر
    clean = re.sub(r'#.*$', '', config)  # حذف تگ
    clean = re.sub(r'[&\?]?[a-z]+=[^&\s]+', '', clean)  # حذف پارامترها
    return hashlib.md5(clean.encode()).hexdigest()

def process_all(texts: List[str]) -> List[str]:
    """پردازش تمام متون استخراج شده"""
    all_configs = []
    seen_hashes = set()
    
    for text in texts:
        configs = extract_configs(text)
        
        for config in configs:
            cleaned = clean_config(config)
            
            if not is_valid(cleaned):
                continue
                
            # حذف تکراری
            config_hash = get_hash(cleaned)
            if config_hash in seen_hashes:
                continue
            seen_hashes.add(config_hash)
            
            all_configs.append(cleaned)
    
    # محدود کردن تعداد
    if len(all_configs) > MAX_CONFIGS:
        import random
        all_configs = random.sample(all_configs, MAX_CONFIGS)
    
    return all_configs
