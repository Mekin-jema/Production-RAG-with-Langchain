import hashlib
import time
from typing import Optional, Any


class ResponseCache:
    """
    In-memory response cache with TTL (time-to-live).

    In production, replace this with Redis for:
    - Persistence across restarts
    - Shared cache across multiple instances
    - Built-in TTL management
    """

    def __init__(
        self,
        ttl_seconds: int = 300,
        max_size: int = 3
    ):
        self.ttl = ttl_seconds
        self.max_size = max_size

        self._cache: dict[str, dict[str, Any]] = {}

        self._hits = 0
        self._misses = 0

    def _make_key(self, query: str) -> str:
        normalized = query.lower().strip()

        return hashlib.sha256(
            normalized.encode("utf-8")
        ).hexdigest()

    def get(self, query: str) -> Optional[str]:
        key = self._make_key(query)

        if key not in self._cache:
            self._misses += 1
            return None

        entry = self._cache[key]

        if time.time() - entry["timestamp"] < self.ttl:
            self._hits += 1
            entry["frequency"] += 1

            return entry["response"]

        del self._cache[key]

        self._misses += 1

        return None

    def set(
        self,
        query: str,
        response: str
    ) -> None:
        key = self._make_key(query)

        if (
            key not in self._cache
            and len(self._cache) >= self.max_size
        ):
            least_used_key = min(
                self._cache,
                key=lambda k: self._cache[k]["frequency"]
            )

            del self._cache[least_used_key]

        self._cache[key] = {
            "response": response,
            "timestamp": time.time(),
            "query": query,
            "frequency": 1
        }

    def clear(self) -> None:
        self._cache.clear()

    @property
    def stats(self) -> dict[str, Any]:
        total = self._hits + self._misses

        hit_rate = (
            self._hits / total * 100
            if total > 0
            else 0
        )

        miss_rate = (
            self._misses / total * 100
            if total > 0
            else 0
        )

        return {
            "hits": self._hits,
            "misses": self._misses,
            "total": total,
            "hit_rate": round(hit_rate, 2),
            "miss_rate": round(miss_rate, 2),
            "cached_entries": len(self._cache)
        }


def demo_cache():
    cache = ResponseCache(
        ttl_seconds=3,
        max_size=3
    )

    print("==== CACHE DEMO ====")
    print()

    result = cache.get("What is Python?")

    print(
        f"1. First lookup: {result} "
        "(Miss - nothing cached yet)"
    )

    cache.set(
        "What is Python?",
        "Python is a programming language."
    )

    print("2. Stored response in cache")

    result = cache.get("What is Python?")

    print(
        f"3. Second lookup: {result} "
        "(Hit!)"
    )

    result = cache.get("what is python?")

    print(
        f"4. Case-insensitive lookup: {result} "
        "(Hit - normalized)"
    )

    result = cache.get("How does AI work?")

    print(
        f"5. Different query: {result} "
        "(Miss!)"
    )

    print(f"6. Stats: {cache.stats}")

    print(
        "Waiting 4 seconds for TTL expiration..."
    )

    time.sleep(4)

    result = cache.get("What is Python?")

    print(
        f"7. Lookup after TTL: {result} "
        "(Miss - expired)"
    )

    print(f"8. Stats: {cache.stats}")

    cache.clear()

    print(
        f"9. Cache cleared. Stats: {cache.stats}"
    )

    print(
        "\n=== EVICTION POLICY TEST (LFU) ==="
    )

    cache = ResponseCache(
        ttl_seconds=60,
        max_size=3
    )

    cache.set("query1", "response1")
    cache.set("query2", "response2")
    cache.set("query3", "response3")

    print(
        f"Initial cache size: "
        f"{cache.stats['cached_entries']}"
    )

    cache.get("query1")
    cache.get("query1")

    cache.set(
        "query4",
        "response4"
    )

    print(
        f"Cache size after adding 4th item: "
        f"{cache.stats['cached_entries']}"
    )

    result = cache.get("query2")

    print(
        f"Lookup query2 after eviction: "
        f"{result} (Miss)"
    )


if __name__ == "__main__":
    demo_cache()