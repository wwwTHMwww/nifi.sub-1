import requests
import base64
import time
from typing import List, Optional, Tuple
from .config import REQUEST_TIMEOUT, USER_AGENT

def fetch_url(url: str) -> Optional[str]:
    """دریافت امن محتوای URL"""
    try:
        headers = {
            'User-Agent': USER_AGENT,
            'Accept': 'text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
        }
        
        response = requests.get(
            url, 
            timeout=REQUEST_TIMEOUT,
            headers=headers,
            allow_redirects=True
        )
        
        if response.status_code != 200:
            return None
            
        # تشخیص encoding
        if response.encoding:
            content = response.text
        else:
            try:
                content = response.content.decode('utf-8')
            except:
                content = response.text
            
        # بررسی base64
        if is_base64(content.strip()):
            try:
                decoded = base64.b64decode(content.strip()).decode('utf-8', errors='ignore')
                if len(decoded) > len(content) * 0.5:
                    return decoded
            except:
                pass
                
        return content
        
    except Exception:
        return None

def is_base64(text: str) -> bool:
    """بررسی base64 بودن متن"""
    if len(text) < 10:
        return False
    try:
        base64.b64decode(text, validate=True)
        return True
    except:
        return False

def fetch_all_sources(sources: List[str]) -> List[str]:
    """دریافت از تمام منابع"""
    results = []
    for url in sources:
        content = fetch_url(url)
        if content:
            results.append(content)
        time.sleep(0.5)  # جلوگیری از محدودیت
    return results
