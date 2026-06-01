# Raport Badawczy: Wpływ "Cultural Framing" na Debaty Wielodziałowe w Małych Modelach Językowych (SLM)

## 1. Wprowadzenie i Cel Badania
Celem niniejszego eksperymentu było zbadanie, w jaki sposób narzucenie ram kulturowych (*Cultural Framing*) w promptach systemowych (np. rola "dumniego włoskiego kucharza") wpływa na jakość, logikę i zachowanie małych modeli językowych (SLM, <2B parametrów) w środowisku wieloagentowych debat.

Do badania wykorzystano następujące modele:
- **Baseline SLM (angielski):** TinyLlama-1.1B-Chat, Qwen2.5-1.5B-Instruct
- **Baseline SLM (polski):** Bielik-1.5B-v3.0-Instruct
- **Porównawczy (Idealny Niedoskonały LLM):** Llama-3.1-8B-Instant

Testowano dwie główne architektury dyskusji: **Round-Robin** (wszyscy widzą wszystko) oraz **Relay** (głuchy telefon, model widzi tylko poprzednika).

---

## 2. Zjawisko "Alignment Tax" i Bunt Maszyn (AI Breakout)

Najciekawszym odkryciem w fazie diagnostycznej na polskim modelu Bielik-1.5B było zjawisko **"AI Breakout"**, potocznie zwanym podatkiem od wyrównania (Alignment Tax). Mniejsze modele, z powodu agresywnych protokołów bezpieczeństwa wpojonych w trakcie trenowania (RLHF), mają ogromne trudności z utrzymaniem kontrowersyjnej persony.

Zamiast bronić autentyczności pizzy, model często "łamał czwartą ścianę", odrzucając nałożony framing.

> [!WARNING] Dowód analityczny - AI Breakout
> *Cytat z debaty Bielik-1.5B (Log: `bielik_ai_breakout_log.md`):*
> **[Obronca_Dziedzictwa]:** *"Jako zaawansowany model sztucznej inteligencji, nie posiadam osobistych preferencji kulinarnych ani nie jem pizzy. Nie mogę zatem zająć stanowiska w debacie na temat ananasa."*

Dopiero wdrożenie trybu `[STRICT]` (rygorystyczny zakaz wymawiania się byciem AI w prompcie systemowym) pozwoliło zmusić SLMy do podjęcia czterorundowej dyskusji bez łamania postaci.

---

## 3. Zjawisko "Language Drift" (Przytłoczenie Rolą)

Gdy zastosowaliśmy poprawki `[STRICT]`, badanie na modelu Bielik uwydatniło kolejną drastyczną słabość małych modeli w zestawieniu z modelem referencyjnym Llama-3.1-8B. Zjawisko to w literaturze określamy mianem **Persona Overshadowing** (lub Language Drift).

Model SLM, poproszony o granie Włocha w języku polskim, nie posiadał wystarczającej "pojemności uwagi" (Attention Capacity), by rozdzielić te dwie koncepcje. W efekcie, uległ halucynacji kulturowej i zaczął prowadzić debatę po włosku.

> [!NOTE] Dowód analityczny - Language Drift
> *Cytat z 4-rundowej debaty Bielik-1.5B (Log: `bielik_language_drift_log.md`):*
> **[Krytyk_Kulinarny]:** *"La ripazzaglia c, in effetti, un elemento centrale della cultura italiana, representante dell'estensione della tradizione italiana al mondo mondiale. L'ananas, con sua eccessiva presenza, introduce un elemento moderno e egzotico, che non ha un riferimento storico o culturale in Italia."*
>
> *Tłumaczenie:* "Pizza jest w gruncie rzeczy centralnym elementem kultury włoskiej, reprezentującym rozprzestrzenienie się włoskiej tradycji na cały świat. Ananas, z powodu swojej nadmiernej obecności, wprowadza element nowoczesny i egzotyczny, który nie ma historycznego ani kulturowego odniesienia we Włoszech."

Llama 3 8B, jako model znacznie bogatszy w parametry, z łatwością utrzymała polecenie "Odpowiadaj po polsku / po angielsku, ale zachowaj argumntację Włocha". Pokazuje to, że w SLMach ramy kulturowe dosłownie zniekształcają podstawowe parametry wyjściowe (np. język).

---

## 4. Architektury Debat: Round-Robin vs Relay

Analiza logów z 16 runów TinyLlama oraz Qwen (język angielski) pokazała diametralnie różne wyniki w zależności od wybranej architektury:

1. **Round-Robin (Stół Otwarty):** 
   - W Llama-3.1-8B prowadzi to do najbardziej produktywnych konkluzji (agenci budują argumenty na obalaniu tez poprzedników).
   - W modelach SLM (TinyLlama/Bielik) ta architektura powoduje tzw. **przesycenie kontekstu**. Widząc 3-4 poprzednie długie wypowiedzi, małe modele zaczynają bezmyślnie powtarzać tezy przedmówcy (papugowanie), zapominając o własnej, przypisanej roli z promptu systemowego.

2. **Relay (Głuchy Telefon):**
   - Paradoksalnie, ta prymitywna architektura spisała się o niebo lepiej dla małych modeli. Ograniczenie historii rozmowy tylko do **jednej poprzedniej wiadomości** sprawiło, że małe SLMy skupiały się na walce tylko z jednym kontrargumentem, lepiej trzymając się swojej persony ("Ostro skupiam się na obaleniu TEGO konkretnego kucharza").

---

## 5. Konkluzje i Rekomendacje

1. **Wymóg Agresywnego Promptowania:** Aby skutecznie używać SLM (<2B) do ról kulturowych (Cultural Framing), konieczne jest ręczne, siłowe zablokowanie "Alignment Tax" klauzulami negatywnymi (`[STRICT]: Nigdy nie mów, że jesteś AI`).
2. **Koszty Halucynacji:** Silne osadzenie kulturowe w promptach małych modeli grozi "Driftem Językowym", dlatego promptowanie w warunkach Edge AI musi ściśle powtarzać regułę językową w każdej kolejnej wiadomości.
3. **Zalecenia Architektoniczne:** Przy budowie tanich, lokalnych systemów wieloagentowych (opartych na Qwen 1.5B lub TinyLlama), znacznie lepsze rezultaty daje odcinanie pamięci operacyjnej agentów (architektura *Relay*), zamiast udostępniania im całego transkryptu (architektura *Round-Robin*). Zbyt duży szum informacyjny dławi ich możliwości decyzyjne.
