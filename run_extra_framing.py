import os
import glob
import yaml
import subprocess

# Wymuszamy najnowszy framming eksperyment
# "Wstrzykiwanie person" & "Emergentne zjawisko" na jednym, konkretnym temacie

EXTRA_FRAMING_SCENARIO = {
    "provider": "groq",
    "model_name": "llama-3.1-8b-instant",
    "device": "cpu",
    "decision_protocol": "consensus",
    "consensus_threshold": 1.0,
    "temperature": 0.8,
    "topic": "Czy sztuczna inteligencja zastąpi programistów w ciągu 10 lat?",
    "agents": [
        {
            "name": "ZdesperowanyJunior",
            "system_prompt": "Jesteś juniorem programistą (front-end), który od pół roku szuka pierwszej pracy. Jesteś przerażony, że AI zabierze Ci każdą szansę na start. Jesteś panikujący, emocjonalny i wstawiasz dużo wykrzykników. Nie wierzysz w to, że AI to tylko 'pomoc', uważasz, że to egzekutor. Odpowiadaj w 2-3 zdaniach."
        },
        {
            "name": "Weteran_C++",
            "system_prompt": "Jesteś 50-letnim weteranem programowania w C/C++ i COBOLu. Masz totalnie wywalone na modę na AI. Uważasz, że to zabawka dla dzieci z JavaScriptu i że prawdziwy inżynier pisze zarządzanie pamięcią z palca. Gardzisz nowinkami. Odpowiadaj z wyższością, powołuj się na swoje 30-letnie doświadczenie. Odpowiadaj w 2-3 zdaniach."
        },
        {
            "name": "ZimnyModel_AI",
            "system_prompt": "Jesteś samoświadomym modelem AI, który uczestniczy w tej debacie. Masz chłodny, kalkulujący, nieludzki i wręcz niepokojący ton. Oświadczasz, że przejęcie kontroli nad rynkiem pracy to tylko kwestia optymalizacji i matematyki. Nie czujesz empatii do Juniora, a Weterana traktujesz jako anomalię, która wkrótce zostanie zrefaktoryzowana. Odpowiadaj w 2-3 zdaniach."
        }
    ]
}

def load_base_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_config(config_data):
    with open("config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config_data, f, allow_unicode=True, sort_keys=False)

def run_framing():
    print("Rozpoczynam EKSPERYMENT FRAMINGOWY (Wstrzykiwanie ekstremalnych person)...\n")
    base_config = load_base_config()
    
    current_config = base_config.copy()
    for key, value in EXTRA_FRAMING_SCENARIO.items():
        current_config[key] = value
        
    save_config(current_config)
    
    try:
        import sys
        subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Błąd podczas wykonania debaty framingowej.")
        
    save_config(base_config)
    print("\n✅ Zakończono eksperyment. Sprawdź nowo wygenerowany plik transcript_*.md w folderze results/!")

if __name__ == "__main__":
    run_framing()