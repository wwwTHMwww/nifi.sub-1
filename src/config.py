import os
import json
from typing import List, Dict, Optional

def load_sources() -> List[str]:
    """بارگذاری لیست منابع از متغیر محیطی"""
    sources_str = os.environ.get('SOURCES', '[]')
    try:
        sources = json.loads(sources_str)
        if not sources:
            # منابع پیش‌فرض
            return [
                "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
                "https://raw.githubusercontent.com/mahdibland/SSAggregator/master/sub/sub_merge.txt",
                "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
            ]
        return sources
    except:
        return []

# تنظیمات
MAX_CONFIGS = 600
MIN_LENGTH = 20
OUTPUT_FILE = "output/sub.txt"
REQUEST_TIMEOUT = 30
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
