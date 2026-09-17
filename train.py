import joblib
import numpy as np
from sklearn.linear_model import LinearRegression

# Données d'exemple : [surface en m2, nombre de pièces]
X = np.array([
    [30, 1],
    [45, 2],
    [60, 2],
    [75, 3],
    [90, 4],
    [120, 5],
    [150, 6]
])

# Prix réels observés (en milliers d'euros)
y = np.array([65, 95, 125, 160, 195, 260, 330])

# Entraînement du modèle
modele = LinearRegression()
modele.fit(X, y)

# Sauvegarde du modèle dans un fichier
joblib.dump(modele, "modele.pkl")
print("Modèle entraîné et sauvegardé sous 'modele.pkl' !")
