import requests

BASE_URL = "https://mon-estimateur-ml-v1-0.onrender.com"
ENDPOINT = f"{BASE_URL}/predire"
API_KEY = "SecretML2026!"

headers = {
    "X-API-Key": API_KEY
}


def estimer_prix(surface: float, nb_pieces: int):
    """Envoie une requête GET sécurisée vers l'API d'estimation."""
    query_params = {
        "surface_m2": surface,
        "pieces": nb_pieces
    }

    try:
        response = requests.get(ENDPOINT, headers=headers, params=query_params, timeout=10)
        
        if response.status_code == 200:
            donnees = response.json()
            print("Réponse reçue avec succès :")
            
            # Récupère la valeur quel que soit le nom exact de la clé
            prix = donnees.get("prix_estime_eur") or donnees.get("prix_estime") or donnees.get("prediction")
            
            print(f"- Surface : {donnees.get('surface_m2')} m²")
            print(f"- Pièces : {donnees.get('pieces')}")
            if prix is not None:
                print(f"- Prix estimé : {float(prix):,.2f} €")
            else:
                print(f"- Données brutes : {donnees}")
            print(f"- Méthode : {donnees.get('methode')}")
            
        elif response.status_code == 401:
            print(f"Accès refusé (401) : {response.json().get('detail')}")
        else:
            print(f"Erreur {response.status_code} : {response.text}")

    except requests.exceptions.RequestException as err:
        print(f"Erreur de connexion : {err}")


if __name__ == "__main__":
    print("--- Test avec authentification valide ---")
    estimer_prix(surface=80, nb_pieces=3)

    print("\n--- Test d'erreur (simulation sans clé) ---")
    req_sans_cle = requests.get(ENDPOINT, params={"surface_m2": 80, "pieces": 3}, timeout=10)
    print(f"Statut sans clé : {req_sans_cle.status_code}")
    print(f"Message : {req_sans_cle.json()}")