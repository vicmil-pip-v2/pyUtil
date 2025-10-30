import os
import random
import time
import urllib.request
import csv
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).resolve().parents[0]))

from fts_search import *


# -------------------------------
# Data generation / CSV
# -------------------------------
def load_word_list(min_words=5000, cache_file="words_alpha.txt") -> list[str]:
    if not os.path.exists(cache_file):
        url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
        print(f"Downloading word list from {url}...")
        data = urllib.request.urlopen(url).read().decode("utf-8")
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(data)
        print(f"Saved to {cache_file}")
    else:
        print(f"Using cached word list: {cache_file}")

    with open(cache_file, "r", encoding="utf-8") as f:
        words = [w.strip().lower() for w in f if len(w.strip()) >= 3]

    print(f"Loaded {len(words):,} words.")
    return random.sample(words, min(min_words, len(words)))

def make_random_phrases(words, num_phrases=20000, min_len=2, max_len=6):
    phrases = []
    for _ in range(num_phrases):
        n = random.randint(min_len, max_len)
        phrases.append(" ".join(random.choices(words, k=n)))
    return phrases

def save_phrases_to_csv(phrases, filename="phrases.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for phrase in phrases:
            writer.writerow([phrase])
    print(f"Saved {len(phrases):,} phrases to {filename}")

# -------------------------------
# Performance test
# -------------------------------
def test_performance():
    DB_FILE = "fts_trigram_perf.db"
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    engine = create_engine(f"sqlite:///{DB_FILE}", echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    TABLE = "perf_test"
    add_fts_table(engine, TABLE)

    # Load words and generate phrases
    words = load_word_list(min_words=20000)
    phrases = make_random_phrases(words, num_phrases=100000)
    save_phrases_to_csv(phrases, filename="phrases.csv")

    # Insert phrases
    print(f"Inserting {len(phrases):,} phrases into SQLite...")
    t0 = time.time()
    insert_fts(session, TABLE, phrases)
    t_insert = time.time() - t0
    print(f"Insertion took {t_insert:.2f}s\n")

    # Test searches
    test_queries = random.sample(words, 10)
    print(f"Testing queries: {test_queries}\n")
    for q in test_queries:
        t1 = time.time()
        res = search_fts(session, TABLE, q, limit=10, offset=0)
        dt = time.time() - t1
        print(f"Query '{q}' → {len(res)} results in {dt:.4f}s")
        if res:
            for r in res[:5]:
                print(f"   • {r}")
        else:
            print("   (no matches)")
        print()

    print("✅ Performance test complete.")

# -------------------------------
# Run test
# -------------------------------
if __name__ == "__main__":
    test_performance()