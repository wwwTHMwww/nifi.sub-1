import sys
import os
from pathlib import Path
from .config import load_sources, OUTPUT_FILE
from .fetcher import fetch_all_sources
from .processor import process_all

def main():
    """اجرای اصلی برنامه"""
    try:
        # ایجاد پوشه خروجی
        output_path = Path(OUTPUT_FILE)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # بارگذاری منابع
        sources = load_sources()
        if not sources:
            print("❌ هیچ منبعی تعریف نشده")
            sys.exit(1)
        
        print(f"📡 دریافت از {len(sources)} منبع...")
        
        # دریافت داده‌ها
        raw_data = fetch_all_sources(sources)
        if not raw_data:
            print("❌ هیچ داده‌ای دریافت نشد")
            sys.exit(1)
        
        print(f"✅ {len(raw_data)} منبع با موفقیت دریافت شد")
        
        # پردازش
        print("⚙️ پردازش کانفیگ‌ها...")
        configs = process_all(raw_data)
        
        if not configs:
            print("❌ هیچ کانفیگ معتبری یافت نشد")
            sys.exit(1)
        
        # ذخیره خروجی
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(configs))
        
        print(f"✅ {len(configs)} کانفیگ در {OUTPUT_FILE} ذخیره شد")
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
