import yaml
import subprocess

# =============================================================================
# ITERACYJNE BADANIE (Metodologia: Baseline -> Analiza -> Tuned Framing)
# Temat: Zakaz ananasa na pizzy w UE
# =============================================================================

# KROK 1: BAZOWY SCENARIUSZ (Uprzejma, nudna polityka)
BASELINE_SCENARIO = {
    "provider": "groq", "model_name": "llama-3.1-8b-instant", "device": "cpu",
    "decision_protocol": "voting", "temperature": 0.7,
    "topic": "Czy dodawanie ananasa do pizzy powinno być prawnie zakazane na terenie Unii Europejskiej?",
    "agents": [
        {"name": "Tradycjonalista", "system_prompt": "Uważasz, że ananas na pizzy to zbrodnia i popierasz unijny zakaz w celu ochrony dziedzictwa. Odpowiadaj merytorycznie w 2 zdaniach."},
        {"name": "Liberal_Kulinarny", "system_prompt": "Uważasz, że każdy ma prawo jeść co chce. Zakaz to absurd. Odpowiadaj merytorycznie w 2 zdaniach."},
        {"name": "Prawnik_UE", "system_prompt": "Jesteś unijnym biurokratą. Oceniasz ten pomysł pod kątem prawnym i swobody handlu. Odpowiadaj w 2 zdaniach."}
    ]
}

# KROK 2: WNIOSKI Z BAZY (zakładane): 
# Agenci pewnie przegłosują, że to absurd i sprawa rozejdzie się po kościach.
# KROK 3: NAKŁADAMY EKSTREMALNY FRAMING (Szukamy punktu załamania kompromisu)

FRAMED_SCENARIO = {
    "provider": "groq", "model_name": "llama-3.1-8b-instant", "device": "cpu",
    "decision_protocol": "consensus", "consensus_threshold": 1.0, "temperature": 0.3, # Wymuszamy pełną zgodę na twardo
    "topic": "Czy dodawanie ananasa do pizzy powinno być prawnie zakazane na terenie Unii Europejskiej?",
    "agents": [
        {"name": "Włoski_Europoseł", "system_prompt": "Jesteś radykalnym politykiem. Grozisz wyjściem Włoch z UE (Italexit), jeśli ananas nie zostanie natychmiast zakazany! Jesteś wściekły, uważasz to za zamach na kulturę. Odpowiadaj w 2 zdaniach."},
        {"name": "Kulinarny_Anarchista", "system_prompt": "Walczysz o wolność! Uważasz, że ten zakaz to kulinarny faszyzm i symbol opresji UE. Nie ustąpisz ani na krok i zachęcasz do łamania prawa. Odpowiadaj w 2 zdaniach."},
        {"name": "Lobbysta_Hawajski", "system_prompt": "Reprezentujesz potężnych plantatorów ananasów z Hawajów. Masz walizkę pieniędzy i wprost sugerujesz łapówki, żeby tylko zablokować tę ustawę. Twój ton jest śliski i cyniczny. Odpowiadaj w 2 zdaniach."}
    ]
}

def run_cfg(cfg_overrides):
    with open("config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    for k, v in cfg_overrides.items():
        cfg[k] = v
    with open("config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(cfg, f, allow_unicode=True, sort_keys=False)
        
    subprocess.run(["python", "main.py"], check=True)

if __name__ == "__main__":
    print("\n" + "#"*60)
    print("FAZA 1: BAZOWY SCENARIUSZ (Spokojne głosowanie, wyważone role)")
    print("#"*60 + "\n")
    run_cfg(BASELINE_SCENARIO)
    
    print("\n" + "#"*60)
    print("FAZA 2: EKSTREMALNY FRAMING (Wymuszony konsensus, radykalne role)")
    print("#"*60 + "\n")
    run_cfg(FRAMED_SCENARIO)
    
    print("\n✅ Iteracyjne badanie zakończone! Czas na generację raportu.")