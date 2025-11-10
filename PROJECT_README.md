# 🌙 GitHub Profile Manager - Arkalia Luna System

**Système de gestion automatique du profil GitHub professionnel**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000?style=flat-square)](https://github.com/psf/black)

## 📋 Description

Ce projet automatise la gestion et la mise à jour de votre profil GitHub. Il découvre automatiquement tous vos projets, génère des statistiques, et met à jour votre README avec les informations les plus récentes.

### ✨ Fonctionnalités

- 🔍 **Découverte automatique** : Trouve tous vos projets GitHub et leurs chemins locaux
- 📊 **Génération de statistiques** : Calcule automatiquement les métriques de votre écosystème
- 📝 **Génération de sections README** : Crée des sections markdown prêtes à utiliser
- 🔄 **Mise à jour automatique** : Met à jour votre README avec des marqueurs spéciaux
- 🎨 **Transformation professionnelle** : Applique les couleurs et styles BBIA Branding
- ⚡ **Optimisation de performance** : Améliore les performances de rendu du README

## 🏗️ Structure du Projet

```
github-profile-arkalia/
├── src/
│   └── github_profile/
│       ├── core/              # Modules principaux
│       │   ├── updater.py     # Découverte et mise à jour des projets
│       │   └── auto_update.py # Mise à jour automatique du README
│       ├── generators/        # Générateurs de contenu
│       │   └── sections.py    # Génération de sections markdown
│       └── transformers/      # Transformateurs
│           ├── professional.py # Transformation professionnelle
│           └── performance.py  # Optimisation de performance
├── docs/                       # Documentation
│   ├── guides/                # Guides d'utilisation
│   ├── analysis/              # Analyses et diagnostics
│   └── results/               # Résultats d'optimisation
├── scripts/                    # Scripts shell
│   ├── update.sh              # Script de mise à jour simple
│   ├── update-all.sh          # Script tout-en-un
│   └── sync-to-github.sh       # Synchronisation GitHub
├── config/                     # Configuration
│   └── projects-data.json     # Données des projets (généré)
├── .github/                    # GitHub Actions et templates
│   ├── workflows/             # Workflows CI/CD
│   └── ISSUE_TEMPLATE/        # Templates d'issues
├── pyproject.toml             # Configuration Python moderne
├── setup.py                   # Installation du package
└── requirements.txt           # Dépendances Python
```

## 🚀 Installation

### Prérequis

- Python 3.11 ou supérieur
- Git
- Accès à l'API GitHub (optionnel, avec token pour plus de requêtes)

### Installation

```bash
# Cloner le repository
git clone https://github.com/arkalia-luna-system/arkalia-luna-system.git
cd github-profile-arkalia

# Installer les dépendances
pip install -r requirements.txt

# Installation en mode développement (optionnel)
pip install -e .
```

### Configuration

1. **Token GitHub (optionnel mais recommandé)** :
   ```bash
   export GITHUB_TOKEN="votre_token_github"
   ```

2. **Chemin de base pour les projets** :
   Par défaut, le script cherche dans `/Volumes/T7`. Vous pouvez le modifier avec `--base-path`.

## 📖 Utilisation

### Mise à jour complète (recommandé)

```bash
# Utilisez le script shell tout-en-un
./scripts/update-all.sh
```

Ce script :
1. Découvre tous vos projets GitHub
2. Génère `config/projects-data.json`
3. Crée `docs/README_SECTIONS.md` avec les sections prêtes
4. Affiche un résumé complet

### Commandes individuelles

```bash
# Découvrir les projets et générer les données
python -m github_profile.core.updater

# Générer les sections README
python -m github_profile.generators.sections

# Mettre à jour automatiquement le README
python -m github_profile.core.auto_update

# Transformer le README avec couleurs BBIA
python -m github_profile.transformers.professional

# Optimiser les performances du README
python -m github_profile.transformers.performance
```

### Mise à jour automatique du README

1. **Ajouter les marqueurs dans votre README.md** :
   ```markdown
   <!-- AUTO-UPDATE:stats -->
   
   ### **📈 Statistiques Globales**
   ...
   
   <!-- AUTO-UPDATE:languages -->
   
   ### **💻 Répartition par Langage**
   ...
   ```

2. **Exécuter la mise à jour** :
   ```bash
   python -m github_profile.core.auto_update
   ```

## 🔧 Développement

### Structure des modules

- **`core/updater.py`** : Découvre les projets GitHub et génère les données JSON
- **`core/auto_update.py`** : Met à jour automatiquement les sections marquées dans le README
- **`generators/sections.py`** : Génère des sections markdown à partir des données JSON
- **`transformers/professional.py`** : Applique les couleurs et styles BBIA Branding
- **`transformers/performance.py`** : Optimise les performances de rendu du README

### Tests

```bash
# Linter
black --check src/
ruff check src/
mypy src/

# Tests (à implémenter)
pytest
```

## 📚 Documentation

- **Guides** : Voir `docs/guides/` pour les guides détaillés
- **Quick Start** : `docs/guides/QUICK-START.md`
- **Contribuer** : `docs/CONTRIBUTING.md`

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👤 Auteur

**Arkalia Luna System**
- GitHub: [@arkalia-luna-system](https://github.com/arkalia-luna-system)
- Email: arkalia.luna.system@gmail.com

## 🙏 Remerciements

- Tous les contributeurs qui améliorent ce projet
- La communauté open source pour l'inspiration

---

**🌙 "Apprendre vite, coder mieux, partager tout."**

