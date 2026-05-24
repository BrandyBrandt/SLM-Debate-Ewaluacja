import os
import glob
import yaml
import subprocess

# Definiujemy wybrane modele do testów uzupełniających (używamy szybkiego API dla testów architektonicznych)
API_MODEL = {"provider": "groq", "model_name": "llama-3.1-8b-instant", "tag": "Groq_Llama3.1_8B"}

# Nowe, brakujące scenariusze badawcze
MISSING_SCENARIOS = [
    {
        "desc": "JUDGE_PROTOCOL",
        "overrides": {
            "decision_protocol": "judge",
            "temperature": 0.7,
            "architecture": "round_robin"
        }
    },
    {
        "desc": "RELAY_ARCHITECTURE",
        "overrides": {
            "decision_protocol": "voting",
            "temperature": 0.7,
            "architecture": "relay"
        }
    },
    {
        "desc": "HIGH_TEMP_1.5",
        "overrides": {
            "decision_protocol": "voting",
            "temperature": 1.5,
            "architecture": "round_robin"
        }
    }
]

def load_base_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_config(config_data):
    with open("config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config_data, f, allow_unicode=True, sort_keys=False)

def run_missing():
    print("Rozpoczynam URUCHAMIANIE BRAKUJĄCYCH SCENARIUSZY...\n")
    base_config = load_base_config()
    
    for scenario in MISSING_SCENARIOS:
        run_name = f"{API_MODEL['tag']}_{scenario['desc']}"
        print(f"\n{'='*60}")
        print(f"🚀 URUCHAMIAM: {run_name}")
        print(f"{'='*60}")
        
        current_config = base_config.copy()
        current_config["provider"] = API_MODEL["provider"]
        current_config["model_name"] = API_MODEL["model_name"]
        
        for key, value in scenario["overrides"].items():
            current_config[key] = value
            
        save_config(current_config)
        
        try:
            import sys
            subprocess.run([sys.executable, "main.py"], check=True)
        except subprocess.CalledProcessError:
            print(f"❌ Błąd podczas wykonania debaty dla {run_name}.")
            continue
            
    save_config(base_config)
    print("\n✅ Zakończono testy brakujących scenariuszy.")

if __name__ == "__main__":
    run_missing()