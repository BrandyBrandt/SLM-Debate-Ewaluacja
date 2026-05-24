# 🚀 Projekt SLM Debate - Instrukcja dla zespołu

Siema! Macie tu gotowy i w 100% zautomatyzowany framework do testowania Małych Modeli Językowych (SLM) w środowisku wieloagentowym. 

Odwaliliśmy całą czarną inżynieryjną robotę. Kod sam zlicza tokeny, weryfikuje konsensus i odpala modele wektorowe, żeby liczyć **Semantic Diversity** (odległość wektorową argumentów) i **Distinct-n** (powtarzalność).

## 🛠 Co my tu mamy?

*   **`config.yaml`** - Główne centrum dowodzenia. Tutaj zmieniacie temat debaty, architekturę, role agentów i temperaturę.
*   **`main.py`** - Silnik debaty. Zrzuci piękny log JSON do folderu `results/`.
*   **`metrics.py`** - Silnik analityczny. Wyliczy naukowe metryki do tabelki.

## 🧪 Jak robić badania (Co już jest gotowe)

Napisaliśmy skrypt **`run_experiments.py`**, który masowo puszcza eksperymenty. Obecnie testuje 4 modele (w tym darmowe API Groq, TinyLlama, Qwen, Phi-3) na dwóch scenariuszach:
1. **SUROWY** - Protokół `voting` (głosowanie).
2. **PODKRĘCONY** - Protokół `consensus` (agenci muszą się zgodzić, próg 100%, niska temperatura, agresywne role Związkowiec vs Korporacjonista).

Odpalcie w terminalu polecenie:
```bash
python run_experiments.py
```
Skrypt wygeneruje pliki `raport_macierz.csv` oraz `PODSUMOWANIE_WYNIKOW.md`. (API Groq wymaga klucza w `.env` ze strony console.groq.com).

## 🎯 Co już przetestowaliśmy? (Gotowe w logach)

Wykonaliśmy już dla Was pełen przekrój zaawansowanych eksperymentów, których wyniki znajdziecie w pliku `PODSUMOWANIE_WYNIKOW.md`:
1. **Różne Protokoły:** Przetestowaliśmy `voting`, agresywny `consensus` (gdzie wyłapywaliśmy uginanie się agentów) oraz protokół `judge` (gdzie niezależny sędzia podsumował całość w sposób bardziej wyważony niż głosowanie tłumu).
2. **Różne Architektury:** Przetestowaliśmy klasyczny `round_robin` oraz głuchy telefon (`relay`). Wnioski jasno pokazują spadek różnorodności semantycznej, gdy agenci mają ograniczoną pamięć.
3. **Ekstremalne Temperatury:** Zrobiliśmy runy z temperaturą 0.2 (upór, sztywność faktów) oraz 1.5 (ogromna kreatywność, ale lekkie gubienie wątku i wybitnie wysoki Distinct-1).

## 💡 Wasze zadanie (Dla chętnych na 5.0)

Mamy kompletny framework i pokryte wszystkie techniczne wymagania dr Okulskiej z pliku z metrykami. 
Jeśli chcecie zabłysnąć na prezentacji, otwórzcie plik `run_experiments.py`, dopiszcie **zupełnie nowy, własny, abstrakcyjny temat dyskusji** (np. dylemat wagonika, spór historyczny) z całkowicie nowymi, przerysowanymi rolami. Puśćcie skrypt, zgarnijcie logi i dodajcie jako Wasz autorski wkład do projektu!

Powodzenia!
