#!/usr/bin/bash

# Vérifier si la commande python existe
if ! command -v python &> /dev/null; then
    echo "La commande 'python' est indisponible. Veuillez installer Python pour continuer, ou ajouter un alias 'alias python=python3' dans votre fichier ~/.bashrc"
    exit 1
fi

# Nom potentiel des répertoires d'environnement
ENV_DIR=""
if [ -d "./venv" ]; then
    ENV_DIR="venv"
elif [ -d "./.venv" ]; then
    ENV_DIR=".venv"
fi

# Si aucun des deux environnements n'existe, en créer un nouveau (par défaut dans .venv)
if [ -z "$ENV_DIR" ]; then
    ENV_DIR=".venv"
    python -m venv "$ENV_DIR"
    echo "Environnement virtuel créé dans $ENV_DIR"
else
    echo "Environnement virtuel déjà existant dans $ENV_DIR"
fi

# Activer l'environnement virtuel
if [ -f "$ENV_DIR/Scripts/activate" ]; then
    # Cas Git Bash sur Windows : Scripts
    source "$ENV_DIR/Scripts/activate"
elif [ -f "$ENV_DIR/bin/activate" ]; then
    # Cas Linux/macOS : bin
    source "$ENV_DIR/bin/activate"
else
    echo "Impossible de trouver le script d'activation de l'environnement virtuel (ni dans Scripts, ni dans bin)."
    exit 1
fi

# Installer les requirements si le fichier requirements.txt existe
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Toutes les dépendances ont été installées dans l'environnement virtuel."
else
    echo "Aucun fichier requirements.txt trouvé, aucune installation réalisée."
fi
