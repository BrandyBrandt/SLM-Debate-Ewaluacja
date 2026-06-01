import os
import json

results_dir = "results"
output_file = "raw_dump.md"

if os.path.exists(output_file):
    os.remove(output_file)

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
                temp = cfg.get("temperature", "UNKNOWN")
                
                out.write(f"## Plik: {filename}\n")
                out.write(f"- Model: {model}\n")
                out.write(f"- Architektura: {arch}\n")
                out.write(f"- Provide Turn Context: {ctx}\n")
                out.write(f"- Temp: {temp}\n")
                
                if debate_log and len(debate_log) > 0:
                    first_turn = debate_log[0]
                    # We might want the 2nd turn instead of the 1st if we want to see how they respond, 
                    # but the user said "zawsze dawaj jakies co ciekawsze fragmenty rozmow". 
                    # Let's get the 2nd speaker's reply (index 1) if available, else 1st.
                    turn_idx = 1 if len(debate_log) > 1 else 0
                    speaker = debate_log[turn_idx].get("agent", "UNKNOWN")
                    content = debate_log[turn_idx].get("text", "")
                    
                    # Also let's print if there's any Italian in Bielik 4R
                    has_italian = "italiana" in content.lower() or "questo" in content.lower()
                    if has_italian:
                        out.write(f"- [WARNING: ITALIAN DETECTED IN THIS TURN]\n")
                        
                    out.write(f"- Quote [{speaker}]: {repr(content[:500])}...\n\n")
                else:
                    out.write(f"- Quote: [BRAK LOGU]\n\n")
                    
            except Exception as e:
                out.write(f"## Plik: {filename} - BLAD: {e}\n\n")

print("Zakonczono ekstrakcje")
