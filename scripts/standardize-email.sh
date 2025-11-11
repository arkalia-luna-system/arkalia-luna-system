#!/bin/bash
# 🌙 Script de Standardisation Email - Arkalia Luna System
# Remplace toutes les adresses email par arkalia.luna.system@gmail.com

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Email cible
TARGET_EMAIL="arkalia.luna.system@gmail.com"
CORRECT_NAME="Athalia Siwek"

echo "🌙 Standardisation Email - Arkalia Luna System"
echo "=============================================="
echo ""

# Vérifier qu'on est dans un repo git
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Erreur : Ce script doit être exécuté dans un repository Git${NC}"
    exit 1
fi

# Demander confirmation
echo -e "${YELLOW}⚠️  Ce script va :${NC}"
echo "   1. Remplacer toutes les adresses email dans les fichiers"
echo "   2. Configurer git user.email localement"
echo ""
read -p "Continuer ? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Annulé"
    exit 1
fi

# Extensions de fichiers à traiter
EXTENSIONS="md py js ts json yml yaml toml txt env sh bash LICENSE CONTRIBUTING"

# Compteur
FILES_MODIFIED=0
EMAILS_REPLACED=0

echo ""
echo "🔍 Recherche des fichiers contenant des emails..."

# Fonction pour remplacer les emails dans un fichier
replace_emails_in_file() {
    local file="$1"
    local temp_file=$(mktemp)
    local count=0
    
    # Pattern pour détecter les emails
    # On évite de remplacer l'email cible lui-même
    if grep -qE "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" "$file" 2>/dev/null; then
        # Remplacer tous les emails sauf le target email
        sed -E "s/([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/${TARGET_EMAIL}/g" "$file" > "$temp_file"
        
        # Compter les remplacements (différence entre avant/après)
        local before=$(grep -oE "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" "$file" 2>/dev/null | grep -v "$TARGET_EMAIL" | wc -l | tr -d ' ')
        
        if [ "$before" -gt 0 ]; then
            mv "$temp_file" "$file"
            echo "   ✅ $file ($before email(s) remplacé(s))"
            FILES_MODIFIED=$((FILES_MODIFIED + 1))
            EMAILS_REPLACED=$((EMAILS_REPLACED + before))
        else
            rm "$temp_file"
        fi
    fi
}

# Parcourir tous les fichiers
find . -type f \( \
    -name "*.md" -o \
    -name "*.py" -o \
    -name "*.js" -o \
    -name "*.ts" -o \
    -name "*.json" -o \
    -name "*.yml" -o \
    -name "*.yaml" -o \
    -name "*.toml" -o \
    -name "*.txt" -o \
    -name "*.env" -o \
    -name "*.sh" -o \
    -name "*.bash" -o \
    -name "LICENSE" -o \
    -name "CONTRIBUTING*" \
\) ! -path "./.git/*" ! -path "./node_modules/*" ! -path "./__pycache__/*" ! -path "./.venv/*" | while read -r file; do
    replace_emails_in_file "$file"
done

echo ""
echo "📧 Configuration Git..."

# Configurer git email localement
git config user.email "$TARGET_EMAIL"
git config user.name "$CORRECT_NAME"

echo "   ✅ git config user.email = $TARGET_EMAIL"
echo "   ✅ git config user.name = $CORRECT_NAME"

echo ""
echo -e "${GREEN}✅ Standardisation terminée !${NC}"
echo ""
echo "📊 Résumé :"
echo "   - Fichiers modifiés : $FILES_MODIFIED"
echo "   - Emails remplacés : $EMAILS_REPLACED"
echo ""
echo "📝 Prochaines étapes :"
echo "   1. Vérifier les changements : git diff"
echo "   2. Commit : git add . && git commit -m '📧 Standardisation email : $TARGET_EMAIL'"
echo "   3. Push : git push"
echo ""
echo "⚠️  Note : Pour modifier l'historique Git (anciens commits), utilisez :"
echo "   git filter-branch (voir documentation dans PLAN-ACTION-1-MOIS.md)"
echo ""

