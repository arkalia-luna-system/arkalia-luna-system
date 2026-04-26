<div align="center">

<img src="https://raw.githubusercontent.com/arkalia-luna-system/arkalia-luna-logo/main/exports/screenshots/ultimate-power-200.svg" alt="Arkalia Luna System" width="80" height="80" style="border-radius: 10px; box-shadow: 0 3px 6px rgba(0,0,0,0.1);" title="Arkalia Luna System" />

# 🚀 Démarrage Rapide - Profile Updater

<img src="https://raw.githubusercontent.com/arkalia-luna-system/bbia_branding/main/logo_2d/final/bbia_mark_only_512x512.png" alt="BBIA Logo" width="60" height="60" style="border-radius: 8px; opacity: 0.9; margin: 10px 0;" title="BBIA" />

**Mise à jour automatique de votre profil GitHub en quelques secondes**

</div>

## ⚡ Utilisation très rapide

```bash
# Option 1: Script shell (le plus simple)
./scripts/update-all.sh

# Option 2: Python direct
python3 update-profile.py
```

**C'est tout !** <img src="https://raw.githubusercontent.com/arkalia-luna-system/bbia_branding/main/logo_2d/final/bbia_favicon_32x32.png" width="16" style="vertical-align: middle; margin: 0 3px; opacity: 0.7; border-radius: 4px;" /> Le script va :
- ✅ Chercher tous vos projets sur GitHub
- ✅ Trouver leurs chemins locaux intelligemment
- ✅ Générer `projects-data.json` avec toutes les infos

## 📋 Ce que vous obtenez

<img src="https://raw.githubusercontent.com/arkalia-luna-system/arkalia-luna-logo/main/exports/screenshots/ai_moon-power-200.svg" width="24" style="float: right; margin: 0 0 10px 15px; opacity: 0.6; border-radius: 6px;" title="Résultats" />

Un fichier `projects-data.json` avec :
- 📦 Liste complète de tous vos projets GitHub
- 🔍 Chemins locaux trouvés automatiquement
- 📄 Chemins des README de chaque projet
- 📊 Statistiques (langages, stars, etc.)

## 🎯 Workflow Recommandé

```bash
# 1. Mettre à jour la liste
./scripts/update-all.sh

# 2. Vérifier les résultats
cat projects-data.json

# 3. Utiliser les données pour mettre à jour votre README.md
```

## 🔧 Options Utiles

```bash
# Mode test (ne modifie rien)
./scripts/update-all.sh --dry-run

# Mode verbeux (voir tous les détails)
./scripts/update-all.sh --verbose

# Chemin personnalisé
./scripts/update-all.sh --base-path /autre/chemin
```

## 💡 Astuce Pro

<img src="https://raw.githubusercontent.com/arkalia-luna-system/bbia_branding/main/logo_2d/final/bbia_favicon_32x32.png" width="18" style="vertical-align: middle; margin: 0 5px; opacity: 0.7; border-radius: 4px;" /> Ajoutez dans votre `~/.zshrc` :

```bash
alias update-profile='cd /Volumes/T7/github-profile-arkalia && ./scripts/update-all.sh'
```

Puis utilisez simplement :
```bash
update-profile
```

## ❓ Problème ?

<img src="https://raw.githubusercontent.com/arkalia-luna-system/arkalia-luna-logo/main/exports/screenshots/advanced-serenity-200.svg" width="20" style="vertical-align: middle; margin: 0 5px; opacity: 0.6; border-radius: 5px;" />

- **"requests non installé"** → `pip3 install requests`
- **"Aucun projet trouvé"** → Vérifiez que vos projets sont dans `/Volumes/T7` ou utilisez `--base-path`
- **"Permission denied"** → `chmod +x scripts/update-all.sh`

---

<div align="center">

<img src="https://raw.githubusercontent.com/arkalia-luna-system/arkalia-luna-logo/main/exports/screenshots/ultimate-power-200.svg" width="30" style="vertical-align: middle; margin: 0 5px; opacity: 0.6;" /> **🌙 C'est tout ! Le script est intelligent et rapide. Utilisez-le à chaque mise à jour de profil !** <img src="https://raw.githubusercontent.com/arkalia-luna-system/bbia_branding/main/logo_2d/final/bbia_mark_only_512x512.png" width="30" style="vertical-align: middle; margin: 0 5px; opacity: 0.8; border-radius: 6px;" />

</div>

