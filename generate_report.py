import os
import glob
import csv
from metrics import DebateEvaluator

def generate_retroactive_transcript(evaluator, json_file):
    """Generuje czytelny transkrypt MD z pliku JSON (retroaktywnie)."""
    base_name = os.path.splitext(os.path.basename(json_file))[0]
    # Usunięcie 'debate_' z przodu jeśli jest, dla czystszej nazwy
    if base_name.startswith("debate_"):
        base_name = base_name[7:]
    
    transcript_file = f"results/transcript_{base_name}.md"
    
    # Pomijamy jeśli już istnieje
    if os.path.exists(transcript_file):
        return
        
    config = evaluator.config
    debate_log = evaluator.debate_log
    decision_result = evaluator.decision
    final_answer = decision_result.get("answer", "")
    decision_name = config.get("decision_protocol", "unknown")
    
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(f"# 🗣️ Transkrypt Debaty\n\n")
        f.write(f"**Temat:** {config.get('topic', 'Brak tematu')}\n")
        f.write(f"**Model:** {config.get('model_name', 'Brak')} ({config.get('provider', 'Brak')})\n")
        f.write(f"**Protokół decyzyjny:** {decision_name}\n\n")
        
        f.write("## 🎭 Uczestnicy\n")
        for a in config.get("agents", []):
            f.write(f"* **{a.get('name', 'Nieznany')}:** _{a.get('system_prompt', 'Brak promptu')}_\n")
            
        f.write("\n## 💬 Przebieg Debaty\n")
        current_round = 0
        for entry in debate_log:
            if entry.get('round', 0) != current_round:
                current_round = entry.get('round', 0)
                f.write(f"\n### 🔔 Runda {current_round}\n\n")
            f.write(f"**[{entry.get('agent', 'Nieznany')}]** ({entry.get('tokens', '?')} tok.):\n{entry.get('text', '')}\n\n")
            
        f.write("## ⚖️ Ostateczna Decyzja\n")
        if "metadata" in decision_result and "log" in decision_result["metadata"]:
            f.write("### Log Konsensusu:\n")
            for log_entry in decision_result["metadata"]["log"]:
                glos = "TAK" if log_entry.get('agrees') else "NIE"
                f.write(f"* {log_entry.get('agent', '')} (Runda {log_entry.get('round', '?')}): **{glos}**\n")
            f.write("\n")
            
        f.write(f"> {final_answer}\n")
        
    print(f"  [+] Wygenerowano wsteczny transkrypt: {transcript_file}")


def generate_full_report():
    print("Generowanie pełnego raportu ze wszystkich plików JSON...")
    files = glob.glob("results/debate_*.json")
    
    if not files:
        print("Brak plików z wynikami!")
        return

    csv_filename = "raport_pelny.csv"
    md_filename = "PODSUMOWANIE_WYNIKOW.md"
    
    csv_headers = [
        "Plik", "Provider", "Model", "Protocol", "Architecture", "Temperature",
        "Tokens/Turn", "Total Flips", "Distinct-1", "Semantic Diversity", "Final Answer"
    ]
    
    all_results = []
    
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_headers)
        
        for file in sorted(files):
            print(f"Przetwarzanie: {file}")
            evaluator = DebateEvaluator(file)
            
            # WSTECZNE GENEROWANIE TRANSKRYPTÓW
            generate_retroactive_transcript(evaluator, file)
            
            metrics = evaluator.evaluate_all()
            
            cfg = evaluator.config
            provider = cfg.get("provider", "unknown")
            model = cfg.get("model_name", "unknown")
            protocol = cfg.get("decision_protocol", "unknown")
            architecture = cfg.get("architecture", "round_robin")
            temperature = cfg.get("temperature", "unknown")
            
            final_ans = str(evaluator.decision.get("answer", ""))[:100].replace('\n', ' ') + "..."
            avg_tok = round(metrics["tokens_per_turn"].get("global_avg", 0), 1) if isinstance(metrics["tokens_per_turn"], dict) else 0
            
            flips = "N/A"
            if isinstance(metrics["flip_rate"], dict):
                flips = metrics["flip_rate"].get("total_flips", 0)
                
            dist1 = metrics["distinct_n"].get("distinct-1", 0) if isinstance(metrics["distinct_n"], dict) else 0
            sem_div = metrics["semantic_diversity"]
            
            writer.writerow([
                os.path.basename(file), provider, model, protocol, architecture, temperature,
                avg_tok, flips, dist1, sem_div, final_ans
            ])
            
            all_results.append({
                "file": os.path.basename(file), "provider": provider, "model": model, 
                "protocol": protocol, "architecture": architecture, "temp": temperature,
                "tokens": avg_tok, "flips": flips, "dist1": dist1, "sem_div": sem_div
            })
            
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write("# 📊 Pełne Podsumowanie Eksperymentów (SLM Debate)\n\n")
        f.write("Poniżej znajduje się automatycznie wygenerowane zestawienie wyników dla **wszystkich** przebiegów, włączając testy Architektury, Temperatury oraz Protokołów Decyzyjnych.\n\n")
        
        f.write("## 🧮 Zaktualizowana Tabela Wyników\n\n")
        f.write("| Model | Protokół | Architektura | Temp | Tokens/Turn | Flip Rate | Distinct-1 | Semantic Div |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for r in all_results:
            model_short = r['model'].split('/')[-1] if '/' in r['model'] else r['model']
            f.write(f"| **{model_short}** | {r['protocol']} | {r['architecture']} | {r['temp']} | {r['tokens']} | {r['flips']} | {r['dist1']} | {r['sem_div']} |\n")
        
        f.write("\n## 📝 Główne Wnioski Zespołu\n")
        f.write("* **Wpływ Temperatury:** Przy temperaturze 1.5 wskaźnik Distinct-1 znacząco rośnie, modele stają się bardziej kreatywne, ale mogą gubić wątek.\n")
        f.write("* **Architektura Relay (Głuchy telefon):** Ograniczenie pamięci agentów do zaledwie poprzedniej wiadomości obniża ich zdolność do nawiązywania do wcześniejszych logicznych argumentów, co widać po zmianach w Różnorodności Semantycznej.\n")
        f.write("* **Protokół Judge vs Voting:** Niezależny Sędzia często wydaje werdykt bardziej bezstronny i kompleksowy niż demokratyczne głosowanie, w którym małe modele często zbyt szybko ulegają presji grupy (szczególnie przy niskiej temperaturze i protokole consensus).\n")
        
    print(f"\n✅ Wygenerowano {csv_filename} oraz {md_filename}!")

if __name__ == "__main__":
    generate_full_report()