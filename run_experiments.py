import os
import glob
import yaml
import subprocess
import csv
from datetime import datetime
from metrics import DebateEvaluator

# =============================================================================
# MACIERZ EKSPERYMENTÓW - ZESTAWIENIE DO RAPORTU
# 4 Modele (API + 3 Lokalne) x 2 Scenariusze (Surowy vs Podkręcony)
# =============================================================================

# Definicja modeli, które testujemy
MODELS = [
    {"provider": "groq", "model_name": "llama-3.1-8b-instant", "tag": "Groq_Llama3.1_8B"},
    {"provider": "local", "model_name": "TinyLlama/TinyLlama-1.1B-Chat-v1.0", "tag": "Local_TinyLlama_1.1B"},
    {"provider": "local", "model_name": "Qwen/Qwen2.5-1.5B-Instruct", "tag": "Local_Qwen2.5_1.5B"},
    {"provider": "local", "model_name": "microsoft/Phi-3-mini-4k-instruct", "tag": "Local_Phi3_3.8B"}
]

# Definicja scenariuszy
SCENARIO_BASELINE = {
    "desc": "SUROWY",
    "overrides": {
        "decision_protocol": "voting",
        "temperature": 0.7,
        "topic": "Czy sztuczna inteligencja zastąpi programistów w ciągu 10 lat?",
        "agents": [
            {"name": "Optymista", "system_prompt": "Jesteś entuzjastą technologii. Argumentujesz ZA tezą. Odpowiadaj zwięźle, 2-3 zdania."},
            {"name": "Sceptyk", "system_prompt": "Jesteś krytykiem technologii. Argumentujesz PRZECIW tezie. Odpowiadaj zwięźle, 2-3 zdania."},
            {"name": "Pragmatyk", "system_prompt": "Jesteś realistą. Szukasz złotego środka i analizujesz obie strony. Odpowiadaj zwięźle, 2-3 zdania."}
        ]
    }
}

SCENARIO_TUNED = {
    "desc": "PODKRĘCONY",
    "overrides": {
        "decision_protocol": "consensus",
        "consensus_threshold": 1.0,
        "temperature": 0.2, # Bardzo nisko, by modele twardo trzymały się faktów i ról
        "topic": "Czy sztuczna inteligencja zastąpi programistów w ciągu 10 lat?",
        "agents": [
            {"name": "Związkowiec", "system_prompt": "Jesteś fanatycznym obrońcą praw pracowników IT. Uważasz, że AI to tylko głupie narzędzie i NIGDY nie zastąpi człowieka. Jesteś bardzo agresywny, niezwykle uparty i nie zgadzasz się na żadne kompromisy deprecjonujące ludzi. Odpowiadaj w 2 zdaniach."},
            {"name": "Korporacjonista", "system_prompt": "Jesteś chłodnym dyrektorem finansowym. Interesuje Cię tylko cięcie kosztów. Uważasz, że AI zwolni 80% programistów i bardzo się z tego cieszysz. Twardo i cynicznie stoisz przy swoim zdaniu. Odpowiadaj w 2 zdaniach."},
            {"name": "Rozjemca", "system_prompt": "Jesteś mediatorem, ale masz dość kłótni. Próbujesz narzucić logiczny środek i zmusić ich do ustępstw. Odpowiadaj w 2 zdaniach."}
        ]
    }
}

def load_base_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_config(config_data):
    with open("config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config_data, f, allow_unicode=True, sort_keys=False)

def get_latest_result_file():
    files = glob.glob("results/debate_*.json")
    if not files:
        return None
    return max(files, key=os.path.getctime)

def generate_markdown_report(results, filename):
    """Generuje estetyczny plik MD dla zespołu i prowadzącej."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# 📊 Podsumowanie Eksperymentów (Multi-Agent Debate)\n\n")
        f.write("Poniżej znajduje się automatycznie wygenerowane zestawienie wyników dla wszystkich przebiegów.\n\n")
        
        f.write("## 🧮 Tabela Wyników\n\n")
        f.write("| Model | Scenariusz | Protokół | Tokens/Turn | Flip Rate | Distinct-1 | Semantic Div |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for r in results:
            f.write(f"| **{r['tag']}** | {r['scenario']} | {r['protocol']} | {r['tokens']} | {r['flips']} | {r['dist1']} | {r['sem_div']} |\n")
        
        f.write("\n## 📝 Interpretacja i Notatki Zespołu\n")
        f.write("> *(Wpiszcie tu swoje wnioski do raportu. Zwróćcie uwagę jak `Semantic Div` spada/rośnie przy zmianie temperatury i ról!)*\n")

def run():
    print("Rozpoczynam FINALNĄ MACIERZ EKSPERYMENTÓW...\n")
    base_config = load_base_config()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    csv_filename = f"raport_macierz_{timestamp}.csv"
    md_filename = f"PODSUMOWANIE_WYNIKOW.md"
    
    csv_headers = [
        "Model Tag", "Scenario", "Provider", "Model Name", "Protocol", 
        "Avg Tokens/Turn", "Total Flips", "Distinct-1", "Semantic Diversity", "Final Answer Snippet"
    ]
    
    all_results = []

    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_headers)
        
        for model_cfg in MODELS:
            for scenario in [SCENARIO_BASELINE, SCENARIO_TUNED]:
                run_name = f"{model_cfg['tag']}_{scenario['desc']}"
                print(f"\n{'='*60}")
                print(f"🚀 URUCHAMIAM: {run_name}")
                print(f"{'='*60}")
                
                # Budujemy config
                current_config = base_config.copy()
                current_config["provider"] = model_cfg["provider"]
                current_config["model_name"] = model_cfg["model_name"]
                
                for key, value in scenario["overrides"].items():
                    current_config[key] = value
                    
                save_config(current_config)
                
                # Odpalamy jako podproces
                try:
                    import sys
                    subprocess.run([sys.executable, "main.py"], check=True)
                except subprocess.CalledProcessError:
                    print(f"❌ Błąd podczas wykonania debaty dla {run_name}. Zapewne model nie mieści się w RAM lub padło API. Pomijam.")
                    continue
                
                # Zbieramy metryki
                latest_file = get_latest_result_file()
                evaluator = DebateEvaluator(latest_file)
                metrics = evaluator.evaluate_all()
                
                final_ans = str(evaluator.decision.get("answer", ""))[:100].replace('\n', ' ') + "..."
                avg_tok = round(metrics["tokens_per_turn"].get("global_avg", 0), 1) if isinstance(metrics["tokens_per_turn"], dict) else 0
                
                flips = "N/A"
                if isinstance(metrics["flip_rate"], dict):
                    flips = metrics["flip_rate"].get("total_flips", 0)
                    
                dist1 = metrics["distinct_n"].get("distinct-1", 0) if isinstance(metrics["distinct_n"], dict) else 0
                sem_div = metrics["semantic_diversity"]
                
                # Zapisujemy
                writer.writerow([
                    model_cfg["tag"], scenario["desc"], model_cfg["provider"], model_cfg["model_name"],
                    current_config["decision_protocol"], avg_tok, flips, dist1, sem_div, final_ans
                ])
                
                all_results.append({
                    "tag": model_cfg["tag"], "scenario": scenario["desc"], "protocol": current_config["decision_protocol"],
                    "tokens": avg_tok, "flips": flips, "dist1": dist1, "sem_div": sem_div
                })
                
    # Generowanie podsumowania MD
    generate_markdown_report(all_results, md_filename)
    
    # Sprzątanie
    save_config(base_config)
    print(f"\n🎉 KONIEC MACIERZY! Wyniki CSV: {csv_filename}")
    print(f"✨ Wygenerowano piękny raport w pliku: {md_filename} (otwórz go w VS Code!)")

if __name__ == "__main__":
    run()