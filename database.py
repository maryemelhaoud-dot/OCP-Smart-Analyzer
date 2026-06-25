import sqlite3
from datetime import datetime

DB_PATH = "database.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Table des lots
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lots (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            p2o5        REAL NOT NULL,
            humidite    REAL NOT NULL,
            temperature REAL NOT NULL,
            qualite     TEXT NOT NULL,
            date        TEXT NOT NULL
        )
    """)

    # Table des prédictions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            lot_id           INTEGER NOT NULL,
            qualite_predite  TEXT NOT NULL,
            confiance        INTEGER NOT NULL,
            date             TEXT NOT NULL,
            FOREIGN KEY (lot_id) REFERENCES lots(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Base de données initialisée")

def ajouter_lot(p2o5, humidite, temperature, qualite):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO lots (p2o5, humidite, temperature, qualite, date)
        VALUES (?, ?, ?, ?, ?)
    """, (p2o5, humidite, temperature, qualite, datetime.now().strftime("%Y-%m-%d %H:%M")))
    lot_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return lot_id

def ajouter_prediction(lot_id, qualite_predite, confiance):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (lot_id, qualite_predite, confiance, date)
        VALUES (?, ?, ?, ?)
    """, (lot_id, qualite_predite, confiance, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()

    # Total des lots
    cursor.execute("SELECT COUNT(*) as total FROM lots")
    total = cursor.fetchone()["total"]

    # Répartition par qualité
    cursor.execute("""
        SELECT qualite, COUNT(*) as count
        FROM lots GROUP BY qualite
    """)
    repartition = {row["qualite"]: row["count"] for row in cursor.fetchall()}

    # P2O5 moyen
    cursor.execute("SELECT AVG(p2o5) as moy FROM lots")
    p2o5_moyen = cursor.fetchone()["moy"] or 0

    # Lots rejetés (qualité C)
    rejetes = repartition.get("C", 0)

    conn.close()
    return {
        "total": total,
        "repartition": repartition,
        "p2o5_moyen": round(p2o5_moyen, 1),
        "rejetes": rejetes,
        "taux_A": round(repartition.get("A", 0) / total * 100, 1) if total > 0 else 0
    }

def get_derniers_lots(limite=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM lots ORDER BY id DESC LIMIT ?
    """, (limite,))
    lots = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return lots

def get_tous_lots():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lots ORDER BY id DESC")
    lots = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return lots

if __name__ == "__main__":
    init_db()
