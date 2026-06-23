import csv
import random

random.seed(42)

def determine_quality(p2o5, humidite, temperature):
    """
    - Qualité A : haute concentration P2O5, faible humidité, température maîtrisée
    - Qualité B : valeurs intermédiaires
    - Qualité C : faible concentration, humidité élevée, température élevée
    """
    score = 0

    if p2o5 >= 31:
        score += 2
    elif p2o5 >= 28:
        score += 1

    if humidite <= 13:
        score += 2
    elif humidite <= 18:
        score += 1

    if temperature <= 48:
        score += 2
    elif temperature <= 55:
        score += 1

    # ajoute un peu de bruit pour rendre le dataset réaliste (pas parfait)
    score += random.choice([-1, 0, 0, 0, 1])

    if score >= 5:
        return "A"
    elif score >= 3:
        return "B"
    else:
        return "C"


rows = []
for i in range(1, 301):
    p2o5 = round(random.uniform(24, 35), 1)
    humidite = round(random.uniform(8, 25), 1)
    temperature = round(random.uniform(35, 65), 1)
    qualite = determine_quality(p2o5, humidite, temperature)

    rows.append({
        "lot_id": f"LOT-{i:04d}",
        "p2o5": p2o5,
        "humidite": humidite,
        "temperature": temperature,
        "qualite": qualite
    })

with open("data/phosphate_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["lot_id", "p2o5", "humidite", "temperature", "qualite"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Dataset généré : {len(rows)} lignes -> data/phosphate_data.csv")

# Petit résumé
from collections import Counter
counts = Counter(r["qualite"] for r in rows)
print("Répartition des qualités :", dict(counts))
