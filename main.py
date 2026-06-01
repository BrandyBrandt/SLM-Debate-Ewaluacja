"""
main.py — Punkt wejścia. Uruchom: python main.py

Krok po kroku:
  1. Wczytaj config.yaml
  2. Załaduj model i tokenizer z Hugging Face
  3. Stwórz agentów i sędziego
  4. Uruchom wybraną architekturę debaty
  5. Wybierz ostateczną decyzję wybranym protokołem (judge/voting/consensus)
"""

import os
import json
import torch
import yaml
from datetime import datetime
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer

from agents import Agent, Judge
from architectures import ARCHITECTURES
from decisions import DECISIONS


def main():
    load_dotenv() # Ładuje klucze z pliku .env
    # 1. Wczytaj config
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 2. Załaduj model (Lokalnie lub przez API Groq)
    provider = config.get("provider", "local")

    if provider == "groq":
        from groq import Groq
        print(f"Ładowanie klienta Groq API (model: {config['model_name']})...")
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "tu_wklej_swoj_klucz_i_zapisz_plik":
            raise ValueError("Brak prawidłowego GROQ_API_KEY w pliku .env! Wklej tam swój klucz z console.groq.com.")
        model = Groq(api_key=api_key)
        tokenizer = None
        print("Klient Groq gotowy.\n")
    else:
        device = config.get("device", "cpu")
        dtype = torch.float16 if device == "cuda" else torch.float32
        load_in_8bit = config.get("load_in_8bit", False)
        
        print(f"Ładowanie modelu lokalnego: {config['model_name']} (8-bit: {load_in_8bit}) na {device}...")
        tokenizer = AutoTokenizer.from_pretrained(config["model_name"])
        
        if load_in_8bit:
            model = AutoModelForCausalLM.from_pretrained(
                config["model_name"],
                load_in_8bit=True,
                device_map="auto"
            )
        else:
            model = AutoModelForCausalLM.from_pretrained(
                config["model_name"], torch_dtype=dtype
            ).to(device)
        print("Model załadowany.\n")

    # 3. Stwórz agentów
    agents = [
        Agent(name=a["name"], system_prompt=a["system_prompt"], model=model, tokenizer=tokenizer)
        for a in config["agents"]
    ]
    judge = Judge(
        system_prompt=config["judge"]["system_prompt"], model=model, tokenizer=tokenizer
    )

    # 4. Uruchom debatę
    arch_name = config["architecture"]
    decision_name = config.get("decision_protocol", "judge")
    run_debate = ARCHITECTURES[arch_name]
    decide = DECISIONS[decision_name]

    print(f"Architektura: {arch_name}")
    print(f"Protokół decyzyjny: {decision_name}")
    print(f"Temat: {config['topic']}")
    print(f"Rundy: {config['num_rounds']}")
    print(f"Agenci: {', '.join(a.name for a in agents)}")

    debate_log = run_debate(agents, judge, config["topic"], config["num_rounds"], config)

    # 5. Wybór ostatecznej decyzji
    decision_result = decide(agents, judge, debate_log, config["topic"], config)
    final_answer = decision_result["answer"]

    print(f"\n{'='*60}")
    print(f"  OSTATECZNA DECYZJA (protokół: {decision_name})")
    print(f"{'='*60}")
    print(f"\n{final_answer}\n")

    # 6. Zapis logów do pliku JSON
    os.makedirs("results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_data = {
        "config": config,
        "debate_log": debate_log,
        "decision": decision_result
    }
    
    output_file = f"results/debate_{timestamp}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print(f"Zapisano pełne logi debaty do: {output_file}")
    
    # 7. Zapis czytelnego transkryptu Markdown
    transcript_file = f"results/transcript_{timestamp}.md"
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(f"# 🗣️ Transkrypt Debaty\n\n")
        f.write(f"**Temat:** {config['topic']}\n")
        f.write(f"**Model:** {config['model_name']} ({config['provider']})\n")
        f.write(f"**Protokół decyzyjny:** {decision_name}\n\n")
        
        f.write("## 🎭 Uczestnicy\n")
        for a in config["agents"]:
            f.write(f"* **{a['name']}:** _{a['system_prompt']}_\n")
            
        f.write("\n## 💬 Przebieg Debaty\n")
        current_round = 0
        for entry in debate_log:
            if entry['round'] != current_round:
                current_round = entry['round']
                f.write(f"\n### 🔔 Runda {current_round}\n\n")
            f.write(f"**[{entry['agent']}]** ({entry.get('tokens', '?')} tok.):\n{entry['text']}\n\n")
            
        f.write("## ⚖️ Ostateczna Decyzja\n")
        if "metadata" in decision_result and "log" in decision_result["metadata"]:
            f.write("### Log Konsensusu:\n")
            for log_entry in decision_result["metadata"]["log"]:
                glos = "TAK" if log_entry['agrees'] else "NIE"
                f.write(f"* {log_entry['agent']} (Runda {log_entry['round']}): **{glos}**\n")
            f.write("\n")
            
        f.write(f"> {final_answer}\n")
        
    print(f"Zapisano czytelny transkrypt do: {transcript_file}")

if __name__ == "__main__":
    main()
