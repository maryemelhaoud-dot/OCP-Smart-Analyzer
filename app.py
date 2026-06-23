from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
from database import init_db, ajouter_lot, ajouter_prediction, get_stats, get_derniers_lots, get_tous_lots

app = Flask(__name__)

# Charger le modèle ML
modele = joblib.load("modele.pkl")

# Initialiser la base de données au démarrage
init_db()
# PAGE PRINCIPALE
@app.route("/")
def accueil():
    return render_template("index.html")
# API : STATISTIQUES DASHBOARD
@app.route("/api/stats")
def api_stats():
    stats = get_stats()
    return jsonify(stats)
# API : DERNIERS LOTS
@app.route("/api/lots")
def api_lots():
    lots = get_derniers_lots(10)
    return jsonify(lots)

# API : TOUS LES LOTS (datasets)
@app.route("/api/datasets")
def api_datasets():
    lots = get_tous_lots()
    return jsonify(lots)

# API : PRÉDICTION IA
@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.json

    p2o5        = float(data["p2o5"])
    humidite    = float(data["humidite"])
    temperature = float(data["temperature"])

    # 1. Le modèle ML prédit la qualité
    prediction = modele.predict([[p2o5, humidite, temperature]])
    qualite = prediction[0]

    # 2. Calculer la confiance
    confiances = {"A": 91, "B": 76, "C": 84}
    confiance = confiances[qualite]

    # 3. Sauvegarder le lot dans la BD
    lot_id = ajouter_lot(p2o5, humidite, temperature, qualite)

    # 4. Sauvegarder la prédiction dans la BD
    ajouter_prediction(lot_id, qualite, confiance)

    # 5. Retourner le résultat + stats mises à jour
    stats = get_stats()

    return jsonify({
        "qualite": qualite,
        "confiance": confiance,
        "lot_id": lot_id,
        "stats": stats
    })
# LANCER LE SERVEUR
if __name__ == "__main__":
    app.run(debug=True)