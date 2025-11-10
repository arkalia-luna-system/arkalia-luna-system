#!/bin/bash
# 🌙 Mise à jour complète du profil GitHub
# Script intelligent qui fait tout automatiquement

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌙 Arkalia Luna System - Mise à Jour Complète${NC}"
echo "============================================================"
echo ""

# 1. Découvrir les projets
echo -e "${BLUE}📡 Étape 1/3 : Découverte des projets...${NC}"
./update.sh

echo ""

# 2. Générer les sections
echo -e "${BLUE}📝 Étape 2/3 : Génération des sections README...${NC}"
python3 generate-readme-sections.py

echo ""

# 3. Afficher un résumé
echo -e "${BLUE}📊 Étape 3/3 : Résumé${NC}"
echo "============================================================"
python3 -c "
import json
from datetime import datetime

try:
    data = json.load(open('projects-data.json'))
    stats = data['stats']
    
    print(f\"✅ Projets totaux:     {stats['total_projects']}\")
    print(f\"✅ Projets locaux:     {stats['local_projects']}/{stats['total_projects']}\")
    print(f\"✅ Avec README:        {stats['projects_with_readme']}/{stats['total_projects']}\")
    print(f\"✅ Langages:           {', '.join(stats['languages'].keys())}\")
    
    # Liste des projets
    print(f\"\n📦 Projets trouvés:\")
    for i, project in enumerate(data['projects'], 1):
        status = '✅' if project.get('local_path') else '🌐'
        name = project['name']
        print(f\"   {i:2d}. {status} {name}\")
    
    print(f\"\n💡 Fichiers générés:\")
    print(f\"   📄 projects-data.json\")
    print(f\"   📄 README_SECTIONS.md\")
    print(f\"\n🚀 Prochaines étapes:\")
    print(f\"   1. Vérifiez README_SECTIONS.md\")
    print(f\"   2. Mettez à jour README.md avec les nouvelles sections\")
    print(f\"   3. (Optionnel) Exécutez: python3 auto-update-readme.py --add-markers\")
    
except Exception as e:
    print(f\"⚠️  Erreur lors de l'affichage du résumé: {e}\")
"

echo ""
echo -e "${GREEN}✅ Mise à jour terminée !${NC}"
echo ""
echo "💡 Pour mettre à jour automatiquement le README :"
echo "   python3 auto-update-readme.py --add-markers"

