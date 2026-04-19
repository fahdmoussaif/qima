# Qima 🚗

**[qimaroc.streamlit.app](https://qimaroc.streamlit.app/)**

Qima est un outil d'estimation du prix des voitures d'occasion au Maroc. Entrez la marque, le modèle, l'année, le kilométrage et le type de carburant — Qima vous donne une estimation du prix de marché en quelques secondes.

---

## Comment ça marche

Les données proviennent de plus de 70 000 annonces scrapées sur Avito.ma. Un modèle de machine learning (LightGBM) a été entraîné sur ces données pour apprendre la relation entre les caractéristiques d'une voiture et son prix de vente réel sur le marché marocain.

---

## Stack

- Python, Requests — scraping Avito.ma
- Pandas, Scikit-learn — nettoyage et préparation des données
- LightGBM — modèle de prédiction
- Streamlit — interface web

---

## Lancer en local

```bash
git clone https://github.com/fahdmoussaif/qima.git
cd qima
pip install -r requirements.txt
streamlit run app.py
```

> Note : vous aurez besoin de `model.pkl` pour faire tourner l'app. Générez-le en exécutant `pipeline.py` avec `avito_cars.csv`.
