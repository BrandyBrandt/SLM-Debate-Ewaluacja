# 🚀 Projekt SLM Debate - Instrukcja dla zespołu

Siema! Macie tu gotowy i w 100% zautomatyzowany framework do testowania Małych Modeli Językowych (SLM) w środowisku wieloagentowym. 

Odwaliliśmy całą czarną inżynieryjną robotę. Nie musicie grzebać w kodzie Pythona, żeby robić badania. Kod sam zlicza tokeny, weryfikuje konsensus i odpala modele wektorowe, żeby liczyć **Semantic Diversity** (odległość wektorową argumentów) i **Distinct-n** (powtarzalność).

## 🛠 Co my tu mamy?

*   **`config.yaml`** - Główne centrum dowodzenia. Tutaj zmieniacie temat debaty, architekturę (np. głuchy telefon vs. wszyscy na raz), role agentów (tzw. persony) i temperaturę.
*   **`main.py`** - Silnik debaty. Jak to odpalicie (`python main.py`), to modele zaczną gadać według configu. Po skończeniu, zrzuci piękny log JSON do folderu `results/`.
*   **`metrics.py`** - Silnik analityczny. Odpalcie to (`python metrics.py`), a skrypt sam weźmie najnowszy plik JSON i wyliczy wam naukowe metryki do tabelki.

## 🧪 Jak robić badania (Szybka ścieżka)

Zamiast odpalać to ręcznie za każdym razem, przygotowaliśmy wam potężny skrypt do masowego puszczania eksperymentów.

1. Otwórzcie plik **`run_experiments.py`**.
2. Zobaczcie na górę pliku. Zdefiniowaliśmy tam 4 modele: Groq API (szybki), TinyLlama, Qwen i potężny Phi-3 z Microsoftu.
3. Skrypt jest tak ustawiony, że puszcza 2 scenariusze:
   *   **SUROWY** (łagodny temat od Inez Okulskiej, spokojne głosowanie).
   *   **PODKRĘCONY** (wymuszony trudny konsensus z agresywnymi rolami: Związkowiec vs. Korporacjonista przy niskiej temperaturze).
4. Odpalcie w terminalu polecenie:
   ```bash
   python run_experiments.py
   ```
5. Idźcie na kawę. Skrypt sam przeładuje modele, podmieni configi, puści 8 potężnych debat i na koniec **wygeneruje pliki `raport_macierz.csv` oraz `PODSUMOWANIE_WYNIKOW.md`**. Wystarczy wkleić tabelkę z MarkDowna prosto do raportu na uczelnię.

## 💡 Co wy musicie zrobić? (Dla chętnych na 5.0)

Jeśli chcecie więcej, po prostu dodajcie do pliku `run_experiments.py` nowe bloki "SCENARIO" (np. scenariusz głuchy telefon, albo scenariusz z mega abstrakcyjnym tematem) i puśćcie skrypt jeszcze raz. Zbierzcie logi z `results/` i wrzućcie wnioski na prezentację. Skupcie się na tym, jak **Semantic Diversity** spada, gdy obniża się temperaturę!

Powodzenia!
