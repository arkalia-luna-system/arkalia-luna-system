#!/bin/bash
# 🌙 Script rapide pour mettre à jour le profil GitHub
# Usage: ./update.sh [options]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌙 Arkalia Luna System - Profile Updater${NC}"
echo "============================================================"

# Vérifie si Python est installé
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}❌ Python3 n'est pas installé${NC}"
    exit 1
fi

# Vérifie si requests est installé
if ! python3 -c "import requests" 2>/dev/null; then
    echo -e "${YELLOW}📦 Installation de 'requests'...${NC}"
    pip3 install -q requests
fi

# Exécute le script Python avec tous les arguments passés
python3 update-profile.py "$@"

# Génère automatiquement les sections README si succès
if [ $? -eq 0 ]; then
    echo -e "\n${BLUE}📝 Génération des sections README...${NC}"
    python3 generate-readme-sections.py 2>/dev/null
fi

echo -e "\n${GREEN}✅ Terminé !${NC}"

