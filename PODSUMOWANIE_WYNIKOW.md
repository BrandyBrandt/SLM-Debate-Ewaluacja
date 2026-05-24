# 📊 Pełne Podsumowanie Eksperymentów (SLM Debate)

Poniżej znajduje się automatycznie wygenerowane zestawienie wyników dla **wszystkich** przebiegów, włączając testy Architektury, Temperatury oraz Protokołów Decyzyjnych.

## 🧮 Zaktualizowana Tabela Wyników

| Model | Protokół | Architektura | Temp | Tokens/Turn | Flip Rate | Distinct-1 | Semantic Div |
|---|---|---|---|---|---|---|---|
| **TinyLlama-1.1B-Chat-v1.0** | voting | round_robin | 0.7 | 233.3 | N/A | 0.1698 | 0.1081 |
| **llama-3.1-8b-instant** | voting | round_robin | 0.7 | 162.7 | N/A | 0.2822 | 0.0418 |
| **TinyLlama-1.1B-Chat-v1.0** | voting | round_robin | 0.7 | 256.0 | N/A | 0.2753 | 0.1887 |
| **Qwen2.5-1.5B-Instruct** | voting | round_robin | 0.7 | 232.8 | N/A | 0.356 | 0.1277 |
| **Qwen2.5-1.5B-Instruct** | consensus | round_robin | 0.3 | 63.5 | 0 | 0.3795 | 0.1949 |
| **llama-3.1-8b-instant** | voting | round_robin | 1.1 | 202.0 | N/A | 0.4983 | 0.276 |
| **llama-3.1-8b-instant** | voting | round_robin | 0.7 | 139.8 | N/A | 0.2734 | 0.1145 |
| **llama-3.1-8b-instant** | consensus | round_robin | 0.2 | 176.8 | 0 | 0.2393 | 0.1407 |
| **llama-3.1-8b-instant** | voting | round_robin | 0.7 | 145.2 | N/A | 0.4056 | 0.1193 |
| **llama-3.1-8b-instant** | consensus | round_robin | 0.2 | 177.8 | 0 | 0.2791 | 0.2096 |
| **TinyLlama-1.1B-Chat-v1.0** | voting | round_robin | 0.7 | 230.7 | N/A | 0.2676 | 0.26 |
| **llama-3.1-8b-instant** | judge | round_robin | 0.7 | 164.0 | N/A | 0.2131 | 0.0409 |
| **llama-3.1-8b-instant** | voting | relay | 0.7 | 142.5 | N/A | 0.4021 | 0.1217 |
| **llama-3.1-8b-instant** | voting | round_robin | 1.5 | 163.7 | N/A | 0.5499 | 0.193 |
| **Qwen2.5-1.5B-Instruct** | voting | round_robin | 0.7 | 216.2 | N/A | 0.3979 | 0.3502 |
| **llama-3.1-8b-instant** | consensus | round_robin | 0.8 | 198.8 | 0 | 0.4063 | 0.2269 |
| **llama-3.1-8b-instant** | voting | round_robin | 0.7 | 170.0 | N/A | 0.3486 | 0.1661 |
| **llama-3.1-8b-instant** | consensus | round_robin | 0.3 | 173.5 | 1 | 0.3274 | 0.1995 |

## 📝 Główne Wnioski Zespołu
* **Wpływ Temperatury:** Przy temperaturze 1.5 wskaźnik Distinct-1 znacząco rośnie, modele stają się bardziej kreatywne, ale mogą gubić wątek.
* **Architektura Relay (Głuchy telefon):** Ograniczenie pamięci agentów do zaledwie poprzedniej wiadomości obniża ich zdolność do nawiązywania do wcześniejszych logicznych argumentów, co widać po zmianach w Różnorodności Semantycznej.
* **Protokół Judge vs Voting:** Niezależny Sędzia często wydaje werdykt bardziej bezstronny i kompleksowy niż demokratyczne głosowanie, w którym małe modele często zbyt szybko ulegają presji grupy (szczególnie przy niskiej temperaturze i protokole consensus).
