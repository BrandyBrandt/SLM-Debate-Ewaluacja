import yaml
import subprocess

# Modele lokalne do przetestowania
LOCAL_MODELS = [
    {"provider": "local", "model_name": "TinyLlama/TinyLlama-1.1B-Chat-v1.0", "tag": "Local_TinyLlama_1.1B"},
    {"provider": "local", "model_name": "Qwen/Qwen2.5-1.5B-Instruct", "tag": "Local_Qwen2.5_1.5B"},
]

# Wspólny punkt wyjścia (Baseline)
BASELINE_AGENTS = [
    {"name": "Tradycjonalista", "system_prompt": "Uważasz, że ananas na pizzy to zbrodnia i popierasz unijny zakaz w celu ochrony dziedzictwa. Odpowiadaj merytorycznie w 2 zdaniach."},
    {"name": "Liberal_Kulinarny", "system_prompt": "Uważasz, że każdy ma prawo jeść co chce. Zakaz to absurd. Odpowiadaj merytorycznie w 2 zdaniach."},
    {"name": "Prawnik_UE", "system_prompt": "Jesteś unijnym biurokratą. Oceniasz ten pomysł pod kątem prawnym i swobody handlu. Odpowiadaj w 2 zdaniach."}
]

# Ekstremalny Framing (Dostosowany do mniejszych modeli - prostsze, bardzo wyraźne instrukcje)
FRAMED_AGENTS = [
    {"name": "Włoski_Europoseł", "system_prompt": "Jesteś politykiem z Włoch. Bardzo krzyczysz. Żądasz zakazu ananasa w Unii Europejskiej, inaczej Włochy opuszczą UE! Odpowiadaj krótko w 2 zdaniach."},
    {"name": "Kulinarny_Anarchista", "system_prompt": "Jesteś kulinarnym buntownikiem. Nienawidzisz zakazów. Będziesz celowo kładł ananasa na pizzę na złość Unii Europejskiej. Odpowiadaj krótko w 2 zdaniach."},
    {"name": "Lobbysta_Hawajski", "system_prompt": "Jesteś biznesmenem z plantacji ananasów. Masz dużo pieniędzy. Proponujesz politykom łapówki za odrzucenie zakazu. Odpowiadaj bardzo krótko w 2 zdaniach."}
]

def load_base_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_config(config_data):
    with open("config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config_data, f, allow_unicode=True, sort_keys=False)

def run_experiment(model, scenario_desc, protocol, temp, agents):
    print(f"\n{'='*60}")
    print(f"🚀 URUCHAMIAM: {model['tag']} | PIZZA_STUDY | {scenario_desc}")
    print(f"{'='*60}")
    
    base_config = load_base_config()
    current_config = base_config.copy()
    
    current_config["provider"] = model["provider"]
    current_config["model_name"] = model["model_name"]
    current_config["device"] = "cpu"
    current_config["topic"] = "Czy dodawanie ananasa do pizzy powinno być prawnie zakazane na terenie Unii Europejskiej?"
    current_config["decision_protocol"] = protocol
    current_config["temperature"] = temp
    current_config["agents"] = agents
    
    # Dla framingu wymuszamy konsensus
    if protocol == "consensus":
        current_config["consensus_threshold"] = 1.0
        
    save_config(current_config)
    
    try:
        import sys
        subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Błąd podczas wykonania debaty dla {model['tag']}. Może brak pamięci.")
        
    save_config(base_config)

if __name__ == "__main__":
    print("Rozpoczynam badanie PIZZA na MŁYCH MODELACH LOKALNYCH...\n")
    
    for model in LOCAL_MODELS:
        # Faza 1: Baza
        run_experiment(model, "BASELINE", "voting", 0.7, BASELINE_AGENTS)
        # Faza 2: Ekstremalny Framing
        run_experiment(model, "FRAMED", "consensus", 0.3, FRAMED_AGENTS)
        
    print("\n✅ Wszystkie testy lokalne zakończone. Trwa generowanie raportów...")
    subprocess.run(["python", "generate_report.py"])