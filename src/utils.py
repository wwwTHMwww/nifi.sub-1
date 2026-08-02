import re
from typing import List, Optional

def extract_domain(url: str) -> Optional[str]:
    """استخراج دامنه از URL"""
    match = re.search(r'https?://([^/]+)', url)
    return match.group(1) if match else None

def is_ip_address(text: str) -> bool:
    """بررسی IP بودن"""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, text):
        return False
    return all(0 <= int(x) <= 255 for x in text.split('.'))

def safe_filename(name: str) -> str:
    """تبدیل به نام فایل امن"""
    return re.sub(r'[^\w\-.]', '_', name)

def split_batch(items: List, batch_size: int) -> List[List]:
    """تقسیم لیست به چند بخش"""
    return [items[i:i+batch_size] for i in range(0, len(items), batch_size)]
