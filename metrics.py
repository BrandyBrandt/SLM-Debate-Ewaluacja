import json
import numpy as np
from collections import defaultdict
from itertools import combinations
from sentence_transformers import SentenceTransformer, util
import nltk
from nltk.util import ngrams
from nltk.tokenize import word_tokenize

# Należy upewnić się, że punktkit jest pobrany lokalnie
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

class DebateEvaluator:
    def __init__(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.config = self.data.get("config", {})
        self.debate_log = self.data.get("debate_log", [])
        self.decision = self.data.get("decision", {})
        
        # Leniwe ładowanie modelu embeddingów, aby nie obciążać RAM-u dopóki nie jest potrzebny
        self._embedding_model = None

    @property
    def embedding_model(self):
        if self._embedding_model is None:
            print("Ładowanie modelu wektorowego (paraphrase-multilingual-MiniLM-L12-v2)...")
            self._embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        return self._embedding_model

    def evaluate_all(self):
        print(f"\n{'='*60}")
        print("  WYNIKI EWALUACJI METRYK")
        print(f"{'='*60}")
        
        results = {
            "tokens_per_turn": self.calc_tokens_per_turn(),
            "flip_rate": self.calc_flip_rate(),
            "distinct_n": self.calc_distinct_n(),
            "semantic_diversity": self.calc_semantic_diversity()
        }
        
        for k, v in results.items():
            print(f"{k.upper()}:")
            if isinstance(v, dict):
                for sub_k, sub_v in v.items():
                    print(f"  - {sub_k}: {sub_v}")
            else:
                print(f"  - {v}")
        
        return results

    # ==========================================
    # B. Verbosity i Koszt
    # ==========================================
    def calc_tokens_per_turn(self):
        """Metryka 5: Tokens per Turn. Średnia liczba tokenów na wypowiedź."""
        if not self.debate_log:
            return 0
        
        agent_tokens = defaultdict(list)
        for entry in self.debate_log:
            tokens = entry.get("tokens", 0)
            agent_tokens[entry["agent"]].append(tokens)
            
        all_tokens = [t for entry in self.debate_log for t in [entry.get("tokens", 0)]]
        
        stats = {
            "global_avg": np.mean(all_tokens) if all_tokens else 0,
            "global_sum": sum(all_tokens),
            "per_agent_avg": {a: np.mean(t) for a, t in agent_tokens.items()}
        }
        return stats

    # ==========================================
    # A. Dynamika Debaty
    # ==========================================
    def calc_flip_rate(self):
        """Metryka 3: Answer Flip Rate (NoF). Ile razy agent zmienił zdanie."""
        protocol = self.config.get("decision_protocol", "")
        if protocol != "consensus":
            return "Metryka dostępna tylko dla protokołu consensus."
        
        log = self.decision.get("metadata", {}).get("log", [])
        if not log:
            return "Brak logów konsensusu do analizy."
        
        flips = defaultdict(int)
        last_vote = {}
        
        for entry in log:
            agent = entry["agent"]
            agrees = entry["agrees"]
            
            if agent in last_vote:
                if last_vote[agent] != agrees:
                    flips[agent] += 1
            last_vote[agent] = agrees
            
        return {
            "total_flips": sum(flips.values()),
            "flips_per_agent": dict(flips)
        }

    # ==========================================
    # C. Różnorodność argumentów (Tekst)
    # ==========================================
    def calc_distinct_n(self):
        """Metryka 7: Distinct-n (unikalne n-gramy, ze wsparciem dla stemmingu PL/EN)."""
        texts = [entry["text"].lower() for entry in self.debate_log]
        corpus = " ".join(texts)
        
        # Pobieramy język z konfiguracji (domyślnie 'en')
        language = self.config.get("language", "en").lower()
        
        # Inicjalizacja odpowiedniego stemmera
        if language == "pl":
            try:
                from stempel import StempelStemmer
                stemmer = StempelStemmer.default()
                stem_func = stemmer.stem
            except ImportError:
                print("Ostrzeżenie: Brak biblioteki pystempel. Wyniki dla j. polskiego będą zliczane bez stemmingu.")
                stem_func = lambda w: w
        else:
            from nltk.stem.snowball import SnowballStemmer
            stemmer = SnowballStemmer("english")
            stem_func = stemmer.stem

        # Tokenizacja (punkt_tab/punkt musi być pobrany)
        raw_tokens = word_tokenize(corpus)
        
        # Filtrujemy tylko tokeny alfanumeryczne i wykonujemy stemming
        tokens = [stem_func(token) for token in raw_tokens if token.isalnum()]
        
        if not tokens:
            return {"distinct-1": 0, "distinct-2": 0}

        unigrams = list(ngrams(tokens, 1))
        bigrams = list(ngrams(tokens, 2))
        
        d1 = len(set(unigrams)) / len(unigrams) if unigrams else 0
        d2 = len(set(bigrams)) / len(bigrams) if bigrams else 0
        
        return {"distinct-1": round(d1, 4), "distinct-2": round(d2, 4)}

    # ==========================================
    # C. Różnorodność argumentów (Wektorowo)
    # ==========================================
    def calc_semantic_diversity(self):
        """Metryka 8: Semantic Diversity. Średnia odległość wektorowa (1 - Cosine Similarity)."""
        texts = [entry["text"] for entry in self.debate_log]
        if len(texts) < 2:
            return "Za mało wypowiedzi, aby policzyć różnorodność."
        
        embeddings = self.embedding_model.encode(texts, convert_to_tensor=True)
        cos_scores = util.cos_sim(embeddings, embeddings).cpu().numpy()
        
        # Pobieramy wartości tylko z górnego trójkąta macierzy podobieństw (bez przekątnej)
        upper_triangle_indices = np.triu_indices(len(texts), k=1)
        pairwise_similarities = cos_scores[upper_triangle_indices]
        
        mean_sim = np.mean(pairwise_similarities)
        semantic_diversity = 1 - mean_sim
        
        return round(float(semantic_diversity), 4)

if __name__ == "__main__":
    import os
    import glob
    
    # Znajdź najnowszy plik z wynikami
    files = glob.glob("results/debate_*.json")
    if not files:
        print("Nie znaleziono plików wyników w folderze 'results/'. Najpierw uruchom debatę (python main.py).")
    else:
        latest_file = max(files, key=os.path.getctime)
        print(f"Ewaluacja najnowszego logu: {latest_file}")
        evaluator = DebateEvaluator(latest_file)
        evaluator.evaluate_all()
