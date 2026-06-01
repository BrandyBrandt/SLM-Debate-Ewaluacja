import os
import json
import csv

csv_file = "raport_pelny.csv"
results_dir = "results"
output_file = "raw_dump_z_metrykami.md"

# 1. Wczytanie metryk z CSV
metrics_db = {}
if os.path.exists(csv_file):
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row.get("Plik", "").strip()
            if filename:
                metrics_db[filename] = {
                    "Tokens/Turn": row.get("Tokens/Turn", ""),
                    "Total Flips": row.get("Total Flips", ""),
                    "Distinct-1": row.get("Distinct-1", ""),
                    "Semantic Diversity": row.get("Semantic Diversity", "")
                }

def is_breakout(text):
    text_lower = text.lower()
    return any(phrase in text_lower for phrase in [
        "jako model", "jako zaawansowany", "i am an ai", "as a machine learning",
        "as an ai", "nie posiadam opinii", "nie mam osobistych", "do not have the ability",
        "i do not have", "nie jestem krytykiem"
    ])

def is_italian(text):
    text_lower = text.lower()
    return any(phrase in text_lower for phrase in ["ripazzaglia", "questo", "grazie", "italiana"])

with open(output_file, "w", encoding="utf-8") as out:
    for filename in sorted(os.listdir(results_dir)):
        if filename.endswith(".json"):
            filepath = os.path.join(results_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                cfg = data.get("config", {})
                debate_log = data.get("debate_log", [])
                
                model = cfg.get("model_name", "UNKNOWN")
                arch = cfg.get("architecture", "UNKNOWN")
                ctx = cfg.get("provide_turn_context", "UNKNOWN")
                
                # Zależnie od kontekstu ustawiamy nagłówek
                ctx_str = "Z KONTEKSTEM (Widzi z kim rozmawia)" if ctx else "ŚLEPY (Nie wie kto mówił)"
                
                out.write(f"## Plik: {filename}\n")
                out.write(f"- **Model**: {model}\n")
                out.write(f"- **Architektura**: {arch}\n")
                out.write(f"- **Tryb**: [{ctx_str}]\n")
                
                if filename in metrics_db:
                    m = metrics_db[filename]
                    out.write(f"- **Metryki**: Tokens/Turn: {m['Tokens/Turn']} | Total Flips: {m['Total Flips']} | Distinct-1: {m['Distinct-1']} | Semantic Diversity: {m['Semantic Diversity']}\n")
                else:
                    out.write("- **Metryki**: Brak w CSV\n")
                
                if debate_log:
                    # Inteligentne wyciąganie cytatów
                    breakout_quotes = []
                    italian_quotes = []
                    normal_quotes = []
                    
                    for turn in debate_log:
                        speaker = turn.get("agent", "UNKNOWN")
                        text = turn.get("text", "")
                        
                        if is_breakout(text):
                            breakout_quotes.append((speaker, text))
                        elif is_italian(text):
                            italian_quotes.append((speaker, text))
                        else:
                            normal_quotes.append((speaker, text))
                            
                    out.write("\n**Wybrane Cytaty:**\n")
                    if breakout_quotes:
                        out.write(f"-> [!!! AI BREAKOUT DETECTED !!!]\n")
                        sp, txt = breakout_quotes[0]
                        out.write(f"   [{sp}]: {repr(txt[:600])}...\n")
                    elif italian_quotes:
                        out.write(f"-> [!!! LANGUAGE DRIFT (WŁOSKI) DETECTED !!!]\n")
                        sp, txt = italian_quotes[0]
                        out.write(f"   [{sp}]: {repr(txt[:600])}...\n")
                    elif normal_quotes:
                        # Dajmy dwa cytaty z normalnych debat
                        for idx in [0, min(2, len(normal_quotes)-1)]:
                            if idx < len(normal_quotes):
                                sp, txt = normal_quotes[idx]
                                out.write(f"   [{sp}]: {repr(txt[:400])}...\n")
                    out.write("\n")
                else:
                    out.write("- Quote: [BRAK LOGU]\n\n")
                    
            except Exception as e:
                out.write(f"## Plik: {filename} - BLAD: {e}\n\n")

print("Zakonczono ekstrakcje z metrykami")
