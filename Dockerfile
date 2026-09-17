FROM python:3.11-slim

# Cr?er un utilisateur standard requis par Hugging Face
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Installer les d?pendances Python
RUN pip install --no-cache-dir --user fastapi uvicorn scikit-learn numpy joblib

# Copier le code dans le conteneur
COPY --chown=user . /app

# Entra?ner le mod?le
RUN python train.py

# D?marrer sur le port 7860 exig? par Hugging Face
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
