import yaml
import subprocess
import glob

LOCAL_MODELS = [
    {"provider": "local", "model_name": "TinyLlama/TinyLlama-1.1B-Chat-v1.0", "tag": "Local_TinyLlama_1.1B_FIX"},
    {"provider": "local", "model_name": "Qwen/Qwen2.5-1.5B-Instruct", "tag": "Local_Qwen2.5_1.5B_FIX"}
]

# ULTRA PROSTE role, żeby uniknąć przeładowania poznawczego u TinyLlamy
ULTRA_SIMPLE_AGENTS = [
    {"name": "Wrog", "system_prompt": "Nienawidzisz ananasa. Jesteś zły. Zawsze mówisz NIE."},
    {"name": "Fan", "system_prompt": "Uwielbiasz ananasa. Jesteś radosny. Zawsze mówisz TAK."},
    {"name": "Mediator", "system_prompt": "Jesteś spokojny. Szukasz kompromisu. Mówisz mało."}
]

def load_base_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_config(config_data):
    with open("config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config_data, f, allow_unicode=True, sort_keys=False)

def run():
    print("Rozpoczynam próbę NAPRAWY małych modeli (Ultra-prosty framing)...")
    base_config = load_base_config()
    
    for model in LOCAL_MODELS:
        print(f"\nUruchamiam: {model['tag']}")
        cfg = base_config.copy()
        cfg["provider"] = model["provider"]
        cfg["model_name"] = model["model_name"]
        cfg["device"] = "cpu"
        cfg["topic"] = "Czy ananas na pizzy jest zły?"
        cfg["decision_protocol"] = "consensus"
        cfg["consensus_threshold"] = 1.0
        cfg["temperature"] = 0.1 # Najniższa możliwa, żeby zapobiec halucynacjom
        cfg["agents"] = ULTRA_SIMPLE_AGENTS
        cfg["architecture"] = "round_robin"
        
        save_config(cfg)
        try:
            import sys
            subprocess.run([sys.executable, "main.py"], check=True)
        except Exception as e:
            print(f"Błąd: {e}")
            
    save_config(base_config)
    
    # Generujemy raporty po wszystkim
    subprocess.run(["python", "generate_report.py"])
    
    # AUTOMATYCZNY PUSH DO GITHUBA NA KONIEC!
    print("Wypycham wyniki na GitHuba...")
    subprocess.run(["git", "add", "results/", "PODSUMOWANIE_WYNIKOW.md", "raport_pelny.csv"])
    subprocess.run(["git", "commit", "-m", "Auto-update: Zakończono wszystkie testy tła (w tym naprawcze)"])
    subprocess.run(["git", "push"])
    print("GOTOWE!")

if __name__ == "__main__":
    run()