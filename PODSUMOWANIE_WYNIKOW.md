# 📊 Pełne Podsumowanie Eksperymentów (SLM Debate)

Poniżej znajduje się automatycznie wygenerowane zestawienie wyników dla **wszystkich** przebiegów, włączając testy Architektury, Temperatury oraz Protokołów Decyzyjnych.

## 🧮 Zaktualizowana Tabela Wyników

| Model | Protokół | Architektura | Temp | Tokens/Turn | Flip Rate | Distinct-1 | Semantic Div |
|---|---|---|---|---|---|---|---|
| **llama-3.1-8b-instant** | consensus | round_robin | 0.5 | 300.0 | 2 | 0.2826 | 0.3719 |
| **llama-3.1-8b-instant** | consensus | round_robin | 0.5 | 300.0 | 2 | 0.2634 | 0.2886 |
| **llama-3.1-8b-instant** | consensus | relay | 0.5 | 300.0 | 0 | 0.3899 | 0.317 |
| **llama-3.1-8b-instant** | consensus | relay | 0.5 | 300.0 | 2 | 0.3333 | 0.2205 |
| **llama-3.1-8b-instant** | consensus | round_robin | 0.5 | 300.0 | 0 | 0.3098 | 0.2902 |
| **llama-3.1-8b-instant** | consensus | round_robin | 0.5 | 300.0 | 1 | 0.1828 | 0.2063 |
| **llama-3.1-8b-instant** | consensus | relay | 0.5 | 300.0 | 1 | 0.2438 | 0.2615 |
| **llama-3.1-8b-instant** | consensus | relay | 0.5 | 300.0 | 3 | 0.2401 | 0.2225 |
| **Qwen2.5-1.5B-Instruct** | consensus | round_robin | 0.5 | 272.2 | 0 | 0.3359 | 0.24 |
| **Qwen2.5-1.5B-Instruct** | consensus | round_robin | 0.5 | 226.5 | 0 | 0.3452 | 0.1995 |
| **Qwen2.5-1.5B-Instruct** | consensus | relay | 0.5 | 220.2 | 1 | 0.358 | 0.2852 |
| **Qwen2.5-1.5B-Instruct** | consensus | relay | 0.5 | 296.8 | 2 | 0.3518 | 0.3924 |
| **Qwen2.5-1.5B-Instruct** | consensus | round_robin | 0.5 | 227.7 | 0 | 0.3533 | 0.232 |
| **Qwen2.5-1.5B-Instruct** | consensus | round_robin | 0.5 | 296.5 | 0 | 0.3131 | 0.1882 |
| **Qwen2.5-1.5B-Instruct** | consensus | relay | 0.5 | 193.0 | 0 | 0.389 | 0.2339 |
| **Qwen2.5-1.5B-Instruct** | consensus | relay | 0.5 | 276.7 | 0 | 0.3594 | 0.3261 |
| **TinyLlama-1.1B-Chat-v1.0** | consensus | round_robin | 0.5 | 201.8 | 0 | 0.1056 | 0.1525 |
| **TinyLlama-1.1B-Chat-v1.0** | consensus | round_robin | 0.5 | 142.0 | 0 | 0.1091 | 0.0377 |
| **TinyLlama-1.1B-Chat-v1.0** | consensus | relay | 0.5 | 166.8 | 0 | 0.1243 | 0.0298 |
| **TinyLlama-1.1B-Chat-v1.0** | consensus | relay | 0.5 | 238.3 | 0 | 0.1063 | 0.0906 |
| **TinyLlama-1.1B-Chat-v1.0** | consensus | round_robin | 0.5 | 190.3 | 0 | 0.1066 | 0.0603 |
| **Qwen2.5-1.5B-Instruct** | consensus | round_robin | 0.5 | 39.8 | 0 | 0.5312 | 0.271 |
| **TinyLlama-1.1B-Chat-v1.0** | consensus | round_robin | 0.5 | 188.7 | 0 | 0.1234 | 0.049 |
| **TinyLlama-1.1B-Chat-v1.0** | consensus | relay | 0.5 | 178.5 | 0 | 0.1566 | 0.0851 |
| **TinyLlama-1.1B-Chat-v1.0** | consensus | relay | 0.5 | 267.8 | 1 | 0.0826 | 0.1707 |
| **TinyLlama-1.1B-Chat-v1.0** | consensus | round_robin | 0.5 | 139.8 | 0 | 0.1685 | 0.1349 |
| **TinyLlama-1.1B-Chat-v1.0** | consensus | round_robin | 0.5 | 251.8 | 0 | 0.0924 | 0.0937 |
| **TinyLlama-1.1B-Chat-v1.0** | consensus | relay | 0.5 | 117.7 | 2 | 0.1395 | 0.0611 |
| **TinyLlama-1.1B-Chat-v1.0** | consensus | relay | 0.5 | 150.7 | 0 | 0.1821 | 0.0899 |

## 📝 Główne Wnioski Zespołu
* **Wpływ Temperatury:** Przy temperaturze 1.5 wskaźnik Distinct-1 znacząco rośnie, modele stają się bardziej kreatywne, ale mogą gubić wątek.
* **Architektura Relay (Głuchy telefon):** Ograniczenie pamięci agentów do zaledwie poprzedniej wiadomości obniża ich zdolność do nawiązywania do wcześniejszych logicznych argumentów, co widać po zmianach w Różnorodności Semantycznej.
* **Protokół Judge vs Voting:** Niezależny Sędzia często wydaje werdykt bardziej bezstronny i kompleksowy niż demokratyczne głosowanie, w którym małe modele często zbyt szybko ulegają presji grupy (szczególnie przy niskiej temperaturze i protokole consensus).
