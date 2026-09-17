import os
import joblib
from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

app = FastAPI(title="API Prédiction Immobilière ML", version="0.2.0")

# Nom de l'en-tête HTTP attendu dans les requêtes
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Récupération de la clé depuis l'environnement Cloud (ou valeur de secours locale)
EXPECTED_API_KEY = os.getenv("API_KEY", "cle-secrete-locale-123")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != EXPECTED_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé d'API invalide ou manquante."
        )
    return api_key

# Chargement du modèle de Machine Learning
model = joblib.load("model.joblib")

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/predire", dependencies=[Depends(verify_api_key)])
def predire_prix(surface_m2: float, pieces: int):
    prediction = model.predict([[surface_m2, pieces]])
    return {
        "surface_m2": surface_m2,
        "pieces": pieces,
        "prix_estime": round(float(prediction[0]), 2)
    }