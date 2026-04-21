import json
import os
import re
from urllib.parse import urlparse

# --- CONFIGURAZIONE ---
URL = "https://en.wikipedia.org/wiki/Quentin_Tarantino"
# ----------------------

def text_to_single_line(text: str) -> str:
    """Rimuove ogni tipo di 'a capo' e spazi multipli."""
    if not text: return ""
    return re.sub(r'\s+', ' ', text).strip()

def aggiorna_json():
    # 1. Trova la cartella esatta dove si trova questo script (aggiorna_gs.py)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Crea i percorsi completi per i file
    html_file_path = os.path.join(BASE_DIR, "input_html.txt")
    gold_file_path = os.path.join(BASE_DIR, "input_gold.txt")
    
    domain = urlparse(URL).netloc.replace("www.", "")
    
    # Crea il percorso per la cartella gs_data
    gs_data_dir = os.path.join(BASE_DIR, "gs_data")
    filepath = os.path.join(gs_data_dir, f"{domain}_gs.json")
    
    # 3. Leggi i contenuti usando i percorsi completi
    try:
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_raw = f.read()
        with open(gold_file_path, "r", encoding="utf-8") as f:
            gold_raw = f.read()
    except FileNotFoundError as e:
        print(f"Errore: Non riesco a trovare i file txt.")
        print(f"Assicurati che si trovino in: {BASE_DIR}")
        return

    # 4. Estrai il titolo dall'HTML
    match_title = re.search(r'<title>(.*?)</title>', html_raw, re.IGNORECASE)
    title = match_title.group(1).strip() if match_title else "Titolo non trovato"

    # 5. Crea il record linearizzato
    nuovo_record = {
        "url": URL,
        "domain": domain,
        "title": title,
        "html_text": text_to_single_line(html_raw),
        "gold_text": text_to_single_line(gold_raw)
    }

    # 6. Salva/Aggiorna nella cartella gs_data
    os.makedirs(gs_data_dir, exist_ok=True)
    
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = [] 
    else:
        data = []

    data.append(nuovo_record)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"--- OPERAZIONE COMPLETATA ---")
    print(f"Record aggiunto a: {filepath}")
    print(f"Dominio: {domain}")

if __name__ == "__main__":
    aggiorna_json()