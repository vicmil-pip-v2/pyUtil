import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# -------------------------------
# FTS5 table setup
# -------------------------------
def add_fts_table(engine, table_name: str):
    """
    Creates a FTS5 virtual table using trigram tokenization.
    """
    conn = engine.raw_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(f"""
            CREATE VIRTUAL TABLE {table_name} 
            USING fts5(string, tokenize='trigram');
        """)
        conn.commit()
    finally:
        conn.close()
    print(f"FTS5 table '{table_name}' created.")


# -------------------------------
# Insert strings in batches
# -------------------------------
def insert_fts(session, table_name: str, strings: list[str], batch_size: int = 1000):
    total = len(strings)
    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        batch = strings[start:end]
        values_clause = ",".join(f"('{s.replace('\'','\'\'')}')" for s in batch)
        session.execute(text(f"INSERT INTO {table_name} (string) VALUES {values_clause}"))
        session.commit()
        print(f"Inserted strings {start + 1} to {end} / {total}")


# -------------------------------
# Search function (handles short queries)
# -------------------------------
def search_fts(session, table_name: str, query: str, limit: int = 10, offset: int = 0) -> list[str]:
    """
    Uses MATCH for queries >=3 characters (trigram search)
    and LIKE for queries <3 characters (single/2-char search).
    """
    if len(query) < 3:
        stmt = text(f"""
            SELECT string FROM {table_name}
            WHERE string LIKE :q
            LIMIT :limit OFFSET :offset
        """)
        res = session.execute(stmt, {"q": f"%{query}%", "limit": limit, "offset": offset})
    else:
        stmt = text(f"""
            SELECT string FROM {table_name} 
            WHERE {table_name} MATCH :q
            LIMIT :limit OFFSET :offset
        """)
        res = session.execute(stmt, {"q": query, "limit": limit, "offset": offset})
    return [r[0] for r in res]


# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    DB_FILE = "fts_trigram.db"
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    engine = create_engine(f"sqlite:///{DB_FILE}", echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    TABLE = "my_strings"
    add_fts_table(engine, TABLE)

    # Example phrases
    phrases = ["racecars", "carpet", "cartoon", "scar", "racingcar", "banana"]
    insert_fts(session, TABLE, phrases)

    # Search examples
    queries = ["car", "a", "race", "scar"]
    for q in queries:
        res = search_fts(session, TABLE, q)
        print(f"Query '{q}' → {res}")
