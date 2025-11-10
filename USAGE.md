<div align="center">

<img src="https://raw.githubusercontent.com/arkalia-luna-system/arkalia-luna-logo/main/exports/screenshots/ultimate-power-200.svg" alt="Arkalia Luna System" width="100" height="100" style="border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" title="Arkalia Luna System" />

# 🌙 Guide d'Utilisation - Profile Updater

<img src="https://raw.githubusercontent.com/arkalia-luna-system/bbia_branding/main/logo_2d/final/bbia_mark_only_512x512.png" alt="BBIA Logo" width="80" height="80" style="border-radius: 10px; opacity: 0.9; margin: 10px 0;" title="BBIA" />

**Guide complet pour mettre à jour automatiquement votre profil GitHub**

</div>

## 🚀 Installation Rapide

```bash
# Installer les dépendances
pip install -r requirements.txt

# Rendre le script exécutable
chmod +x update-profile.py
```

## 📖 Utilisation de Base

### 1. Découvrir tous vos projets

```bash
python update-profile.py
```

<img src="https://raw.githubusercontent.com/arkalia-luna-system/bbia_branding/main/logo_2d/final/bbia_favicon_32x32.png" width="18" style="float: right; margin: 0 0 10px 15px; opacity: 0.7; border-radius: 4px;" title="Processus" />

Le script va :
- ✅ Se connecter à votre GitHub (`arkalia-luna-system`)
- ✅ Lister tous vos repos publics
- ✅ Chercher intelligemment les chemins locaux (sans fouiller tout le T7)
- ✅ Trouver les README de chaque projet
- ✅ Générer un fichier `projects-data.json` avec toutes les infos

### 2. Mode Test (Dry-Run)

```bash
python update-profile.py --dry-run
```

Affiche ce qui serait fait sans rien modifier.

### 3. Export Personnalisé

```bash
python update-profile.py --export mon-export.json
```

## 🔧 Options Avancées

### Token GitHub (Optionnel mais Recommandé)

Pour plus de requêtes API et de meilleures performances :

```bash
export GITHUB_TOKEN="votre_token_github"
python update-profile.py
```

**Comment obtenir un token :**
1. GitHub → Settings → Developer settings → Personal access tokens
2. Générer un token avec scope `public_repo`
3. L'exporter dans votre terminal

### Chemin Personnalisé

Si vos projets sont ailleurs que `/Volumes/T7` :

```bash
python update-profile.py --base-path /chemin/vers/vos/projets
```

### Mode Verbeux

Pour voir tous les détails :

```bash
python update-profile.py --verbose
```

## 📊 Fichier de Sortie

Le script génère `projects-data.json` avec :

```json
{
  "username": "arkalia-luna-system",
  "generated_at": "2025-01-XX...",
  "stats": {
    "total_projects": 11,
    "local_projects": 8,
    "projects_with_readme": 8,
    "total_stars": 42,
    "languages": {
      "Python": 8,
      "HTML": 2,
      "JavaScript": 1
    }
  },
  "projects": [
    {
      "name": "arkalia-luna-pro",
      "github_url": "https://github.com/arkalia-luna-system/arkalia-luna-pro",
      "local_path": "/Volumes/T7/arkalia-luna-pro",
      "readme_path": "/Volumes/T7/arkalia-luna-pro/README.md",
      "description": "...",
      "language": "Python",
      "stars": 5,
      "is_public": true
    }
  ]
}
```

## 🎯 Workflow Recommandé

### À chaque mise à jour de profil :

```bash
# 1. Mettre à jour la liste des projets
python update-profile.py

# 2. Vérifier le fichier généré
cat projects-data.json

# 3. Utiliser les données pour mettre à jour README.md
# (manuellement ou avec un autre script)
```

### Automatisation (Optionnel)

Ajoutez dans votre `.zshrc` ou `.bashrc` :

```bash
alias update-github-profile='cd /Volumes/T7/github-profile-arkalia && python update-profile.py'
```

Puis utilisez simplement :
```bash
update-github-profile
```

## 🧠 Comment ça marche ?

### Recherche Intelligente

Le script cherche les projets dans cet ordre :
1. Chemins directs probables (`/Volumes/T7/nom-projet`)
2. Sous-dossiers connus (max 2 niveaux)
3. Vérifie que c'est un repo Git (présence de `.git`)
4. Trouve le README racine automatiquement

**Il ne fouille PAS tout le T7** - seulement les chemins probables.

### Performance

- ✅ Utilise l'API GitHub (pas de scraping)
- ✅ Recherche limitée à 2 niveaux de profondeur
- ✅ Cache les résultats dans JSON
- ✅ Timeout de 10s par requête API

## ❓ Problèmes Courants

### "requests non installé"
```bash
pip install requests
```

### "Aucun projet trouvé localement"
Vérifiez que :
- Vos projets sont bien dans `/Volumes/T7` ou un sous-dossier
- Les noms de dossiers correspondent aux noms GitHub
- Les repos ont un dossier `.git`

### "Rate limit GitHub"
Définissez `GITHUB_TOKEN` pour plus de requêtes.

## 🎉 C'est tout !

<div align="center">

<img src="https://raw.githubusercontent.com/arkalia-luna-system/arkalia-luna-logo/main/exports/screenshots/ultimate-power-200.svg" width="40" style="vertical-align: middle; margin: 0 5px; opacity: 0.7;" /> **Vous êtes maintenant prêt à maintenir votre profil GitHub à jour automatiquement !** <img src="https://raw.githubusercontent.com/arkalia-luna-system/bbia_branding/main/logo_2d/final/bbia_mark_only_512x512.png" width="40" style="vertical-align: middle; margin: 0 5px; opacity: 0.85; border-radius: 8px;" />

*Le script est intelligent, rapide et respecte votre structure de fichiers existante.*

</div>

Le script est conçu pour être **simple, rapide et intelligent**. 
Utilisez-le à chaque fois que vous voulez mettre à jour votre profil GitHub !

