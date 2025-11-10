# 🏗️ Structure du Projet - GitHub Profile Manager

## 📁 Organisation des Fichiers

```
github-profile-arkalia/
│
├── 📂 src/                          # Code source Python
│   └── github_profile/
│       ├── __init__.py             # Package principal
│       ├── core/                    # Modules principaux
│       │   ├── __init__.py
│       │   ├── updater.py          # Découverte et mise à jour des projets
│       │   └── auto_update.py      # Mise à jour automatique du README
│       ├── generators/              # Générateurs de contenu
│       │   ├── __init__.py
│       │   └── sections.py         # Génération de sections markdown
│       └── transformers/            # Transformateurs
│           ├── __init__.py
│           ├── professional.py    # Transformation professionnelle (BBIA)
│           └── performance.py     # Optimisation de performance
│
├── 📂 docs/                         # Documentation
│   ├── CONTRIBUTING.md             # Guide de contribution
│   ├── README_SECTIONS.md          # Sections générées (auto)
│   ├── guides/                     # Guides d'utilisation
│   │   ├── QUICK-START.md
│   │   ├── GUIDE-UTILISATION-INTELLIGENTE.md
│   │   ├── GUIDE-TRANSFORMATION-PROFESSIONNELLE.md
│   │   └── ...
│   ├── analysis/                    # Analyses et diagnostics
│   │   ├── ANALYSE-STRUCTURE-PROFESSIONNELLE.md
│   │   ├── DIAGNOSTIC-PERFORMANCE.md
│   │   └── ...
│   └── results/                     # Résultats d'optimisation
│       ├── RESULTAT-OPTIMISATION.md
│       └── ...
│
├── 📂 scripts/                      # Scripts shell
│   ├── update.sh                   # Script de mise à jour simple
│   ├── update-all.sh               # Script tout-en-un
│   └── sync-to-github.sh           # Synchronisation GitHub
│
├── 📂 config/                       # Configuration
│   ├── config.example.json         # Exemple de configuration
│   └── projects-data.json          # Données des projets (généré)
│
├── 📂 .github/                      # GitHub Actions et templates
│   ├── workflows/
│   │   ├── update-profile.yml      # Mise à jour automatique du profil
│   │   └── ci.yml                 # CI/CD
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
│
├── 📄 README.md                     # README principal (profil GitHub)
├── 📄 PROJECT_README.md             # README du projet lui-même
├── 📄 STRUCTURE.md                  # Ce fichier
├── 📄 LICENSE                       # Licence MIT
├── 📄 pyproject.toml                # Configuration Python moderne
├── 📄 setup.py                      # Installation du package
├── 📄 requirements.txt              # Dépendances Python
└── 📄 .gitignore                    # Fichiers ignorés par Git
```

## 🔄 Migration depuis l'Ancienne Structure

### Fichiers Déplacés

| Ancien Emplacement | Nouveau Emplacement |
|-------------------|---------------------|
| `update-profile.py` | `src/github_profile/core/updater.py` |
| `auto-update-readme.py` | `src/github_profile/core/auto_update.py` |
| `generate-readme-sections.py` | `src/github_profile/generators/sections.py` |
| `transform-to-professional.py` | `src/github_profile/transformers/professional.py` |
| `optimize-performance.py` | `src/github_profile/transformers/performance.py` |
| `update.sh` | `scripts/update.sh` |
| `update-all.sh` | `scripts/update-all.sh` |
| `projects-data.json` | `config/projects-data.json` |
| `README_SECTIONS.md` | `docs/README_SECTIONS.md` |
| Tous les `.md` de guides | `docs/guides/` |

### Commandes Mises à Jour

#### Anciennes commandes (ne fonctionnent plus)
```bash
python update-profile.py
python auto-update-readme.py
python generate-readme-sections.py
./update.sh
```

#### Nouvelles commandes
```bash
# Utilisation en module Python
python -m github_profile.core.updater
python -m github_profile.core.auto_update
python -m github_profile.generators.sections

# Ou via les scripts shell (recommandé)
./scripts/update-all.sh

# Ou après installation
update-profile
generate-sections
auto-update
```

## 🎯 Utilisation de la Nouvelle Structure

### 1. Installation

```bash
# Installation en mode développement
pip install -e .
```

### 2. Utilisation des Scripts

```bash
# Script tout-en-un (recommandé)
./scripts/update-all.sh

# Scripts individuels
python -m github_profile.core.updater
python -m github_profile.generators.sections
python -m github_profile.core.auto_update
```

### 3. Configuration

Les fichiers de configuration sont maintenant dans `config/` :
- `config/projects-data.json` : Données générées automatiquement
- `config/config.example.json` : Exemple de configuration

## 📊 Avantages de la Nouvelle Structure

✅ **Organisation claire** : Séparation logique du code, docs, scripts, config
✅ **Installation en package** : Peut être installé avec `pip install -e .`
✅ **Modules réutilisables** : Code organisé en modules Python
✅ **Documentation centralisée** : Tous les guides dans `docs/`
✅ **CI/CD intégré** : Workflows GitHub Actions prêts
✅ **Standards Python** : `pyproject.toml`, structure moderne
✅ **Facilité de maintenance** : Structure professionnelle et scalable

## 🔧 Développement

### Ajouter un nouveau module

1. Créer le fichier dans le bon dossier (`core/`, `generators/`, ou `transformers/`)
2. Ajouter l'import dans `__init__.py` si nécessaire
3. Ajouter l'entry point dans `pyproject.toml` si c'est un script CLI
4. Tester avec `python -m github_profile.votre_module`

### Ajouter de la documentation

1. Guides → `docs/guides/`
2. Analyses → `docs/analysis/`
3. Résultats → `docs/results/`

## 📝 Notes

- Les anciens scripts à la racine sont toujours présents pour compatibilité
- La structure est rétrocompatible avec les chemins relatifs
- Les workflows GitHub Actions utilisent la nouvelle structure

---

**🌙 Structure créée le : 2025-11-10**
**Dernière mise à jour : Automatique via GitHub Actions**

