import streamlit as st
import pickle
import pandas as pd

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Qima — Estimation Auto",
    page_icon="🚗",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:       #0a0a0a;
    --surface:  #141414;
    --border:   #242424;
    --accent:   #e8ff47;
    --text:     #f0f0f0;
    --muted:    #666;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none; }
#MainMenu, footer, header { visibility: hidden; }

.hero {
    text-align: center;
    padding: 3rem 0 2rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.5rem, 6vw, 4rem);
    font-weight: 800;
    line-height: 1.1;
    color: var(--text);
    margin: 0 0 1rem;
}
.hero-title span { color: var(--accent); }
.hero-sub {
    font-size: 1rem;
    color: var(--muted);
    font-weight: 300;
    margin: 0;
}

.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

.result-box {
    background: var(--accent);
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    margin: 2rem 0;
}
.result-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #0a0a0a;
    opacity: 0.6;
    margin-bottom: 0.5rem;
}
.result-price {
    font-size: 10rem;
    font-weight: 800;
    color: #0a0a0a;
    margin: 0;
    line-height: 1.2;
    letter-spacing: -0.02em;
}
.result-range {
    font-size: 0.9rem;
    color: #0a0a0a;
    opacity: 0.6;
    margin-top: 0.75rem;
}

.stats-row {
    display: flex;
    gap: 1rem;
    margin: 1rem 0;
}
.stat-card {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
}
.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent);
}
.stat-label {
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 0.25rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] > div > div > input {
    background: #1e1e1e !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}
label { color: var(--muted) !important; font-size: 0.85rem !important; }

[data-testid="stButton"] { width: 100% !important; }
[data-testid="stButton"] > button {
    background: var(--accent) !important;
    color: #0a0a0a !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    cursor: pointer !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stButton"] > button:hover {
    background: #d4eb30 !important;
}

.disclaimer {
    text-align: center;
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

try:
    data           = load_model()
    model          = data["model"]
    label_encoders = data["label_encoders"]
    features       = data["features"]
    brand_models   = data["brand_models"]
    brands         = sorted(data["brands"])
    fuels          = sorted(data["fuels"])
    transmissions  = sorted(data["transmissions"])
except FileNotFoundError:
    st.error("model.pkl not found — run pipeline.py first.")
    st.stop()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1 class="hero-title">Qima<br><span>votre voiture</span></h1>
    <p class="hero-sub">Estimation instantanée basée sur 70 000+ annonces Avito.ma</p>
</div>
""", unsafe_allow_html=True)

# ── Form ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Informations du véhicule</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    brand = st.selectbox("Marque", ["Sélectionner..."] + brands)
with col2:
    if brand and brand != "Sélectionner...":
        available_models = ["Autre"] + sorted(brand_models.get(brand, []))
    else:
        available_models = ["Autre"]
    model_name = st.selectbox("Modèle", available_models)

col3, col4 = st.columns(2)
with col3:
    year = st.number_input("Année", min_value=1990, max_value=2026, value=2018, step=1)
with col4:
    mileage = st.number_input("Kilométrage (km)", min_value=0, max_value=500000, value=100000, step=5000)

col5, col6 = st.columns(2)
with col5:
    fuel = st.selectbox("Carburant", fuels)
with col6:
    transmission = st.selectbox("Boîte de vitesses", transmissions)

# ── Predict ───────────────────────────────────────────────────────────────────
def encode(col, val):
    le = label_encoders[col]
    if val in le.classes_:
        return le.transform([val])[0]
    return le.transform(["Autre"])[0]

def predict(brand, model_name, year, mileage, fuel, transmission):
    age            = 2026 - year
    mileage_per_yr = min(mileage / max(age, 1), 100000)

    row = pd.DataFrame([{
        "year":             year,
        "age":              age,
        "mileage":          mileage,
        "mileage_per_year": mileage_per_yr,
        "brand_enc":        encode("brand", brand),
        "model_enc":        encode("model", model_name),
        "fuel_enc":         encode("fuel", fuel),
        "transmission_enc": encode("transmission", transmission),
        "city_enc":         0,
    }])

    price = model.predict(row[features])[0]
    low   = price * 0.88
    high  = price * 1.12
    return price, low, high

st.markdown("<br>", unsafe_allow_html=True)
estimate_clicked = st.button("Estimer le prix →")

if estimate_clicked:
    if brand == "Sélectionner...":
        st.warning("Veuillez sélectionner une marque.")
    else:
        price, low, high = predict(
            brand, model_name, year, mileage, fuel, transmission
        )

        st.markdown(f"""
        <div class="result-box">
            <p class="result-label">Prix estimé</p>
            <p class="result-price">{price:,.0f} DH</p>
            <p class="result-range">Entre {low:,.0f} et {high:,.0f} DH</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-value">{2026 - year} ans</div>
                <div class="stat-label">Âge du véhicule</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{mileage/1000:.0f}k km</div>
                <div class="stat-label">Kilométrage</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{min(mileage/max(2026-year,1), 100000):,.0f}</div>
                <div class="stat-label">km / an</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
    Estimation basée sur les annonces Avito.ma · Précision moyenne ±24 000 DH · À titre indicatif uniquement
</div>
""", unsafe_allow_html=True)
