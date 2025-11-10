#!/bin/bash
# 🌙 Mise à jour complète du profil GitHub
# Script intelligent qui fait tout automatiquement

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🌙 Arkalia Luna System - Mise à Jour Complète${NC}"
echo "============================================================"
echo ""

# 1. Découvrir les projets et générer projects-data.json
echo -e "${BLUE}📡 Étape 1/2 : Découverte des projets depuis GitHub...${NC}"
python3 update-profile.py --export config/projects-data.json || {
    echo -e "${YELLOW}⚠️  Erreur lors de la découverte des projets${NC}"
    exit 1
}

echo ""

# 2. Mettre à jour le README automatiquement
echo -e "${BLUE}📝 Étape 2/2 : Mise à jour du README...${NC}"
python3 auto-update-readme.py || {
    echo -e "${YELLOW}⚠️  Erreur lors de la mise à jour du README${NC}"
    exit 1
}

echo ""
echo -e "${GREEN}✅ Mise à jour terminée !${NC}"
echo ""
echo "💡 Fichiers mis à jour :"
echo "   📄 config/projects-data.json"
echo "   📄 README.md"
