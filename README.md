# OCP Smart Analyzer

Application web intelligente d'analyse et de prédiction de la qualité des lots de phosphate, basée sur le Machine Learning.

## Description

OCP Smart Analyzer permet de prédire automatiquement la qualité d'un lot de phosphate (**A**, **B** ou **C**) à partir de trois mesures :
- la teneur en **P2O5**
- le taux d'**humidité**
- la **température**

Le modèle de prédiction est un **RandomForestClassifier** (scikit-learn), entraîné sur un jeu de données simulé. L'application propose également un tableau de bord avec des statistiques en temps réel (répartition des qualités, taux de lots A, lots rejetés, P2O5 moyen, etc.).

## Fonctionnalités

-  Prédiction de la qualité d'un lot via un modèle de Machine Learning
-  Tableau de bord avec statistiques en temps réel
-  Historique des lots et des prédictions sauvegardé en base SQLite
-  Interface web responsive (Flask + HTML/CSS/JS + Chart.js)

## Stack technique

| Composant       | Technologie                |
|-----------------|--------------------------- |
| Backend         | Python, Flask              |
| Machine Learning| scikit-learn (RandomForest)|
| Base de données | SQLite                     |
| Frontend        | HTML, CSS, JavaScript, Chart.js |

## Structure du projet

```
ocp-smart-analyzer/
├── app.py                  # Application Flask (routes + API)
├── database.py             # Gestion de la base de données SQLite
├── model.py                # Entraînement du modèle ML
├── modele.pkl              # Modèle entraîné (généré)
├── database.db             # Base de données (générée)
├── data/
│   ├── generate_data.py    # Génération du dataset simulé
│   └── phosphate_data.csv  # Dataset des lots de phosphate
├── templates/
│   └── index.html          # Interface utilisateur
├── requirements.txt
└── .gitignore
```

## Installation

1. Cloner le dépôt
```bash
git clone https://github.com/maryemelhaoud-dot/OCP-Smart-Analyzer.git
cd OCP-Smart-Analyzer
```

2. Créer un environnement virtuel (recommandé)
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS / Linux
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

## Utilisation

1. **Générer le dataset** (si besoin)
```bash
python data/generate_data.py
```

2. **Entraîner le modèle**
```bash
python model.py
```
Cela crée le fichier `modele.pkl` utilisé par l'application.

3. **Lancer l'application**
```bash
python app.py
```

4. Ouvrir un navigateur à l'adresse :
```
http://127.0.0.1:5000
```

## API

| Endpoint            | Méthode | Description                          |
|----------------------|---------|---------------------------------------|
| `/api/stats`         | GET     | Statistiques globales du dashboard    |
| `/api/lots`          | GET     | Les 10 derniers lots ajoutés          |
| `/api/datasets`      | GET     | Tous les lots enregistrés             |
| `/api/predict`       | POST    | Prédit la qualité d'un nouveau lot    |

**Exemple de requête `/api/predict` :**
```json
{
  "p2o5": 31.5,
  "humidite": 12.0,
  "temperature": 45.0
}
```

**Réponse :**
```json
{
  "qualite": "A",
  "confiance": 91,
  "lot_id": 1,
  "stats": { ... }
}
```

## Auteur

Maryem El Haoud

## Licence

Projet réalisé à des fins d'apprentissage / démonstration.
