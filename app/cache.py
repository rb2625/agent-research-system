import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "cache_store.json")
SIMILARITY_THRESHOLD = 0.45


class SemanticCache:
    def __init__(self, path: str = CACHE_FILE, threshold: float = SIMILARITY_THRESHOLD):
        self.path = path
        self.threshold = threshold
        self.entries = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)
        return []

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.entries, f, indent=2)

    def get(self, query: str):
        if not self.entries:
            return None

        queries = [entry["query"] for entry in self.entries] + [query]
        vectorizer = TfidfVectorizer().fit(queries)
        vectors = vectorizer.transform(queries)

        similarities = cosine_similarity(vectors[-1], vectors[:-1])[0]
        best_index = int(similarities.argmax())
        best_score = float(similarities[best_index])

        if best_score >= self.threshold:
            return self.entries[best_index]["response"]
        return None

    def set(self, query: str, response):
        self.entries.append({"query": query, "response": response})
        self._save()