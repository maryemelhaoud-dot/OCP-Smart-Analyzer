import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# 1. Charger les données
df = pd.read_csv("data/phosphate_data.csv")
print("Dataset chargé :", df.shape)
print(df["qualite"].value_counts())

# 2. Préparer X (entrées) et y (sortie à prédire)
X = df[["p2o5", "humidite", "temperature"]]
y = df["qualite"]

# 3. Séparer en données d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Entraîner le modèle
modele = RandomForestClassifier(n_estimators=100, random_state=42)
modele.fit(X_train, y_train)
print("Modèle entraîné !")

# 5. Tester la précision
predictions = modele.predict(X_test)
precision = accuracy_score(y_test, predictions)
print(f"Précision du modèle : {precision * 100:.1f}%")

# 6. Sauvegarder le modèle
joblib.dump(modele, "modele.pkl")
print("Modèle sauvegardé -> modele.pkl")