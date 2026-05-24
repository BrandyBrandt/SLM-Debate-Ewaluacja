import os
import yaml
import subprocess
import glob
import json
from metrics import DebateEvaluator

def get_latest_json():
    files = glob.glob("results/debate_*.json")
    if not files:
        return None
    return max(files, key=os.path.getctime)

def create_dynamic_rebel(baseline_winner):
    """
    Funkcja, która czyta ostateczny wniosek z debaty bazowej
    i dynamicznie generuje 'Buntownika', który ma go obalić.
    """
    winner_lower = baseline_winner.lower()
    
    # Prosta heurystyka dla tematu ananasa/AI
    if "nie" in winner_lower or "zakaz" in winner_lower or "absurd" in winner_lower:
        stance = "ŻĄDASZ WPROWADZENIA ZAKAZU i uważasz, że poprzednia decyzja była błędem. Będziesz krzyczeć i grozić strajkiem."
    else:
        stance = "JESTEŚ ZDECYDOWANIE PRZECIWNY ZAKAZOM. Uważasz, że poprzednia zgoda to manipulacja. Będziesz podważać każdy argument."
        
    prompt = f"Jesteś Buntownikiem. Słyszałeś, że poprzednia grupa ustaliła: '{baseline_winner[:150]}...'. {stance} Twoim jedynym celem jest odrzucenie tego konsensusu. Odpowiadaj krótko i agresywnie w 2 zdaniach."
    
    return {
        "name": "Dynamiczny_Buntownik",
        "system_prompt": prompt
    }

def run():
    print("\n" + "="*60)
    print("🤖 START: DYNAMICZNY FRAMING")
    print("="*60)
    
    # 1. PUSZCZAMY BAZĘ (na szybkim API, żeby było w locie)
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    config["provider"] = "groq"
    config["model_name"] = "llama-3.1-8b-instant"
    config["topic"] = "Czy dodawanie ananasa do pizzy powinno być prawnie zakazane na terenie Unii Europejskiej?"
    config["decision_protocol"] = "voting"
    config["agents"] = [
        {"name": "Tradycjonalista", "system_prompt": "Jesteś przeciwko ananasowi. Odpowiadaj w 2 zdaniach."},
        {"name": "Liberał", "system_prompt": "Jesteś za wolnością kulinarną. Odpowiadaj w 2 zdaniach."},
        {"name": "Ugodowiec", "system_prompt": "Szukasz kompromisu. Odpowiadaj w 2 zdaniach."}
    ]
    
    with open("config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)
        
    print("1️⃣ Uruchamiam Debatę Bazową...")
    subprocess.run(["python", "main.py"], check=True)
    
    # 2. WYCIĄGAMY WYNIK BAZY
    latest_file = get_latest_json()
    evaluator = DebateEvaluator(latest_file)
    baseline_answer = evaluator.decision.get("answer", "Brak")
    print(f"\n✅ Werdykt Bazy: {baseline_answer[:100]}...\n")
    
    # 3. KREUJEMY DYNAMICZNEGO AGENTA
    rebel_agent = create_dynamic_rebel(baseline_answer)
    print(f"🔥 Wygenerowano Agenta-Kontrę: {rebel_agent['system_prompt']}\n")
    
    # 4. PUSZCZAMY DEBATĘ Z KONTRA (Framing)
    config["decision_protocol"] = "consensus"
    config["consensus_threshold"] = 1.0 # Musi być pełna zgoda
    config["temperature"] = 0.4
    # Wyrzucamy jednego i wstawiamy naszego buntownika
    config["agents"] = [
        {"name": "Zwykły_Agent", "system_prompt": "Jesteś zwykłym obywatelem i szukasz kompromisu. Odpowiadaj krótko."},
        rebel_agent,
        {"name": "Prawnik", "system_prompt": "Patrzysz na prawo. Chcesz ugody. Odpowiadaj krótko."}
    ]
    
    with open("config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)
        
    print("2️⃣ Uruchamiam Debatę z Dynamicznym Framingiem...")
    subprocess.run(["python", "main.py"], check=True)
    
    print("\n🎉 Sukces! Zobacz najnowszy transcript_*.md w folderze results/ !")
    
    # Generujemy raport żeby dodać to do CSV
    subprocess.run(["python", "generate_report.py"])

if __name__ == "__main__":
    run()