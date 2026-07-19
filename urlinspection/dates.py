import os
import re

# --- AYARLAR ---
CONTENT_DIR = "content"
LANGS_TO_SYNC = ["tr", "de"]
MASTER_LANG = "en"

def get_date_from_file(filepath):
    """Dosyadan date değerini çeker."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'^date\s*:\s*(.*)$', content, re.MULTILINE)
            return match.group(1).strip() if match else None
    except Exception:
        return None

def sync_dates():
    master_path = os.path.join(CONTENT_DIR, MASTER_LANG)
    
    # 1. Önce İngilizce (Master) klasöründeki tüm dosyaları ve tarihlerini haritala
    master_dates = {}
    for root, dirs, files in os.walk(master_path):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, master_path)
                date_val = get_date_from_file(full_path)
                if date_val:
                    master_dates[rel_path] = date_val

    # 2. TR ve DE klasörlerini gez ve tarihleri Master ile eşitle
    for lang in LANGS_TO_SYNC:
        lang_path = os.path.join(CONTENT_DIR, lang)
        for rel_path, master_date in master_dates.items():
            target_file = os.path.join(lang_path, rel_path)
            
            if os.path.exists(target_file):
                with open(target_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Mevcut tarihi Master tarih ile değiştir
                if re.search(r'^date\s*:', content, re.MULTILINE):
                    new_content = re.sub(r'^date\s*:\s*.*$', f'date: {master_date}', content, flags=re.MULTILINE)
                    
                    with open(target_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"[{lang.upper()}] Senkronize Edildi: {rel_path} -> {master_date}")

if __name__ == "__main__":
    sync_dates()