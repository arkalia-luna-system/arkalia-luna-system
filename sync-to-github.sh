#!/bin/bash

# 🚀 Script de synchronisation automatique du profil GitHub
# Usage: ./sync-to-github.sh

echo "🚀 Synchronisation du profil GitHub Arkalia Luna System..."
echo ""

# Vérifier qu'on est dans le bon dossier
if [ ! -f "README.md" ]; then
    echo "❌ Erreur: README.md non trouvé"
    echo "Lance ce script depuis /Volumes/T7/github-profile-arkalia/"
    exit 1
fi

# Vérifier si le repository existe
if [ ! -d ".git" ]; then
    echo "📂 Initialisation du repository local..."
    git init
    git remote add origin https://github.com/arkalia-luna-system/arkalia-luna-system.git
fi

# Vérifier les changements
echo "🔍 Vérification des changements..."
if git status --porcelain | grep -q .; then
    echo "✅ Changements détectés, synchronisation..."
    
    # Ajouter les fichiers
    git add .
    
    # Commit avec horodatage
    git commit -m "update: profil organisation $(date +'%Y-%m-%d %H:%M')"
    
    # Push vers GitHub
    echo "📤 Push vers GitHub..."
    if git push origin main; then
        echo "✅ Profil synchronisé avec succès !"
        echo ""
        echo "🌐 Ton profil est maintenant visible sur :"
        echo "   https://github.com/arkalia-luna-system/arkalia-luna-system"
        echo ""
        echo "⏰ Attendre 2-3 minutes pour que GitHub affiche les changements"
    else
        echo "❌ Erreur lors du push"
        echo ""
        echo "📋 Solution manuelle :"
        echo "1. Va sur https://github.com/arkalia-luna-system/arkalia-luna-system"
        echo "2. Édite README.md"
        echo "3. Colle le contenu de ton fichier local"
    fi
else
    echo "📄 Aucun changement détecté"
fi

echo ""
echo "🎉 Script terminé !"
