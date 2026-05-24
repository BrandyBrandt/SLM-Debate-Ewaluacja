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

## 🎯 ZADANIA DLA WAS (Czego jeszcze NIE przetestowaliśmy!)

Zrobiliśmy fundamenty, ale żeby raport był kompletny, musicie dodać własne scenariusze do pliku `run_experiments.py` w liście `EXPERIMENTS`. **Co zostało do zrobienia?**

1. **Test protokołu JUDGE:** Mamy 3 protokoły (`voting`, `consensus`, `judge`). Przetestowaliśmy dwa pierwsze. Zróbcie scenariusz, w którym `decision_protocol: "judge"` i sprawdźcie czy niezależny Sędzia radzi sobie lepiej niż głosowanie tłumu!
2. **Test Architektury (Głuchy telefon):** Zmieńcie architekturę komunikacji. Dodajcie parametr `architecture: "relay"` (agenci widzą tylko poprzednią wypowiedź, a nie całą historię) i sprawdźcie, jak bardzo spadnie "Semantic Diversity".
3. **Zabawa temperaturą:** Zróbcie ekstremalny scenariusz z temperaturą `1.5` i luźnym tematem.
4. **Wasz własny, abstrakcyjny temat:** Wymyślcie zupełnie nowe role (np. Prawnik vs 12-letni Haker) i stwórzcie własny scenariusz.

Zmieniajcie, odpalajcie i zbierajcie wnioski do tabelki! Powodzenia!
