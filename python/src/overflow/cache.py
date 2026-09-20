import json
import math
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


def _tokens(text):
    return TOKEN_PATTERN.findall(text.lower())


def _vector(text):
    counts = {}
    for token in _tokens(text):
        counts[token] = counts.get(token, 0) + 1
    return counts


def _cosine(a, b):
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    dot = sum(a[k] * b[k] for k in common)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class SemanticCache:
    def __init__(self, path=None, threshold=0.85):
        if path is None:
            path = Path.cwd() / ".overflow" / "cache" / "cache.db"
        self.path = Path(path)
        self.threshold = threshold
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(str(self.path))

    def _init_db(self):
        conn = self._connect()
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS entries ("
                "id TEXT PRIMARY KEY,"
                "vector TEXT NOT NULL,"
                "response TEXT NOT NULL,"
                "provider TEXT NOT NULL,"
                "created TEXT NOT NULL)"
            )
            conn.commit()
        finally:
            conn.close()

    def get(self, text, provider=None):
        target = _vector(text)
        conn = self._connect()
        try:
            if provider is None:
                rows = conn.execute(
                    "SELECT vector, response, provider FROM entries"
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT vector, response, provider FROM entries WHERE provider = ?",
                    (provider,)
                ).fetchall()
        finally:
            conn.close()

        best = None
        best_score = 0.0

        for vector_json, response, row_provider in rows:
            score = _cosine(target, json.loads(vector_json))
            if score > best_score:
                best_score = score
                best = (response, row_provider)

        if best is None or best_score < self.threshold:
            return None

        return {
            "response": best[0],
            "provider": best[1],
            "similarity": round(best_score, 4)
        }

    def put(self, text, response, provider):
        entry_id = str(uuid.uuid4())
        vector_json = json.dumps(_vector(text), sort_keys=True)
        created = datetime.now(timezone.utc).isoformat()
        conn = self._connect()
        try:
            conn.execute(
                "INSERT OR REPLACE INTO entries (id, vector, response, provider, created) VALUES (?, ?, ?, ?, ?)",
                (entry_id, vector_json, response, provider, created)
            )
            conn.commit()
        finally:
            conn.close()

    def stats(self):
        conn = self._connect()
        try:
            count = conn.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
        finally:
            conn.close()
        return {
            "entries": count,
            "threshold": self.threshold,
            "path": str(self.path)
        }
