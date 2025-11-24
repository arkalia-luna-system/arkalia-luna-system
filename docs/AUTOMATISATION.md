# 🔄 Guide Complet de l'Automatisation

**Date :** 24 novembre 2025  
**Objectif :** Documenter complètement le système d'automatisation du profil GitHub

---

## 🎯 Vue d'Ensemble

Ce projet automatise complètement la mise à jour du profil GitHub avec :

1. **Découverte automatique** des projets depuis GitHub
2. **Génération automatique** des métriques
3. **Mise à jour automatique** du README
4. **CI/CD automatisée** pour tout synchroniser

---

## 📁 Architecture des Scripts

### 1. `update-profile.py` - Découverte des Projets

**Rôle :** Découvre tous les projets GitHub et génère `config/projects-data.json`

**Fonctionnalités :**
- Récupère tous les repos via GitHub API
- Cherche les chemins locaux intelligemment
- Extrait les descriptions depuis les README
- Détecte les langages secondaires
- Génère `config/projects-data.json` avec toutes les infos

**Usage :**
```bash
python update-profile.py --export config/projects-data.json
python update-profile.py --verbose  # Mode verbeux
python update-profile.py --dry-run  # Test sans modification
```

**Fichier généré :** `config/projects-data.json`

---

### 2. `auto-update-readme.py` - Mise à Jour du README

**Rôle :** Met à jour automatiquement les sections marquées dans README.md

**Fonctionnalités :**
- Lit `config/projects-data.json`
- Génère automatiquement :
  - Section statistiques (`<!-- AUTO-UPDATE:stats -->`)
  - Tableau des projets (`<!-- AUTO-UPDATE:projects -->`)
  - Section langages (`<!-- AUTO-UPDATE:languages -->`)
- Dates dynamiques en français

**Usage :**
```bash
python auto-update-readme.py
python auto-update-readme.py --dry-run  # Test sans modification
python auto-update-readme.py --add-markers  # Ajoute les marqueurs si absents
```

**Marqueurs supportés :**
- `<!-- AUTO-UPDATE:stats -->` : Statistiques globales
- `<!-- AUTO-UPDATE:projects -->` : Tableau des projets
- `<!-- AUTO-UPDATE:languages -->` : Liste des langages

---

### 3. `scripts/update_readme_metrics.py` - Mise à Jour des Métriques

**Rôle :** Met à jour les métriques depuis `arkalia-metrics-collector`

**Fonctionnalités :**
- Lit `arkalia-metrics-collector/metrics/aggregated_metrics.json`
- Met à jour les badges et chiffres dans README
- Dates dynamiques en français
- Formatage des nombres avec séparateurs

**Usage :**
```bash
python scripts/update_readme_metrics.py
```

**Fichier source :** `arkalia-metrics-collector/metrics/aggregated_metrics.json`

---

### 4. `scripts/create_badges_metrics.py` - Génération des Badges

**Rôle :** Génère les badges Shields.io pour les métriques

**Fonctionnalités :**
- Crée des badges personnalisés
- Export en Markdown
- Intégration avec les métriques

**Usage :**
```bash
python scripts/create_badges_metrics.py
```

---

### 5. `scripts/update-all.sh` - Script Tout-en-Un

**Rôle :** Exécute toutes les mises à jour en une seule commande

**Fonctionnalités :**
- Appelle `update-profile.py`
- Appelle `auto-update-readme.py`
- Gestion d'erreurs
- Messages colorés

**Usage :**
```bash
./scripts/update-all.sh
```

---

## 🔄 Workflow Complet

### Workflow Manuel

1. **Découvrir les projets :**
   ```bash
   python update-profile.py --export config/projects-data.json
   ```

2. **Mettre à jour le README :**
   ```bash
   python auto-update-readme.py
   ```

3. **Mettre à jour les métriques :**
   ```bash
   python scripts/update_readme_metrics.py
   ```

**Ou tout en une fois :**
```bash
./scripts/update-all.sh
```

### Workflow Automatique (CI/CD)

#### 1. Mise à Jour du Profil (Hebdomadaire)

**Fichier :** `.github/workflows/update-profile.yml`

**Déclenchement :**
- Tous les dimanches à 2h UTC
- Manuellement via `workflow_dispatch`

**Actions :**
1. Checkout repository
2. Setup Python
3. Découvre les projets (`update-profile.py`)
4. Met à jour le README (`auto-update-readme.py`)
5. Commit et push automatique

#### 2. Mise à Jour des Métriques (Quotidienne)

**Fichier :** `.github/workflows/update-metrics.yml`

**Déclenchement :**
- Tous les jours à 2h UTC
- Manuellement via `workflow_dispatch`

**Actions :**
1. Checkout repository principal
2. Checkout `arkalia-metrics-collector`
3. Exécute l'agrégation des métriques
4. Met à jour README avec métriques (`update_readme_metrics.py`)
5. Crée les badges (`create_badges_metrics.py`)
6. Commit et push automatique

#### 3. CI (Lint & Tests)

**Fichier :** `.github/workflows/ci.yml`

**Déclenchement :**
- Sur push vers `main` ou `develop`
- Sur pull request vers `main` ou `develop`

**Actions :**
1. Lint avec Black
2. Lint avec Ruff
3. Type checking avec MyPy
4. Tests (à implémenter)

---

## 📊 Structure des Données

### `config/projects-data.json`

Structure :
```json
{
  "username": "arkalia-luna-system",
  "generated_at": "2025-11-24T...",
  "stats": {
    "total_projects": 11,
    "local_projects": 1,
    "projects_with_readme": 1,
    "total_stars": 0,
    "languages": {
      "Python": 10,
      "Dart": 1
    }
  },
  "projects": [
    {
      "name": "bbia-sim",
      "github_url": "https://github.com/...",
      "local_path": null,
      "readme_path": null,
      "description": "...",
      "language": "Python",
      "stars": 0,
      "is_public": true
    }
  ]
}
```

### `arkalia-metrics-collector/metrics/aggregated_metrics.json`

Structure :
```json
{
  "aggregated": {
    "total_modules": 52320,
    "total_tests": 11204,
    "total_lines_of_code": 24790076,
    "total_documentation_files": 6530,
    "global_coverage": 64.5
  },
  "projects": [
    {
      "name": "bbia-sim",
      "tests": 1362,
      "coverage": 68.86
    }
  ]
}
```

---

## 🎯 Sections Automatisées dans README.md

### 1. Statistiques (`<!-- AUTO-UPDATE:stats -->`)

**Généré par :** `auto-update-readme.py`

**Contenu :**
- Nombre de projets
- Liste des langages avec comptage
- Date de mise à jour dynamique

### 2. Tableau des Projets (`<!-- AUTO-UPDATE:projects -->`)

**Généré par :** `auto-update-readme.py`

**Colonnes :**
- Projet (avec lien GitHub)
- Description
- Stack (détecté automatiquement)
- Rôle (🏢 Prod, 🔧 Tooling, 📦 Archive)
- Status (✅ Production, 🚧 Beta, etc.)

**Détection automatique :**
- Stack : Analyse description et nom
- Rôle : Analyse nom et description
- Status : Analyse nom et description

### 3. Langages (`<!-- AUTO-UPDATE:languages -->`)

**Généré par :** `auto-update-readme.py`

**Contenu :** Liste des langages avec comptage

---

## 🔧 Configuration

### Variables d'Environnement

- `GITHUB_TOKEN` : Token GitHub pour API (optionnel mais recommandé)

### Fichiers de Configuration

- `config/projects-data.json` : Données des projets (généré automatiquement)
- `requirements.txt` : Dépendances Python
- `pyproject.toml` : Configuration du projet

---

## 🚀 Utilisation Rapide

### Pour Mettre à Jour Tout le Profil

```bash
# Option 1 : Script tout-en-un
./scripts/update-all.sh

# Option 2 : Commandes séparées
python update-profile.py --export config/projects-data.json
python auto-update-readme.py
python scripts/update_readme_metrics.py
```

### Pour Tester Sans Modifier

```bash
python update-profile.py --dry-run
python auto-update-readme.py --dry-run
```

### Pour Ajouter les Marqueurs Automatiquement

```bash
python auto-update-readme.py --add-markers
```

---

## 📝 Exemples d'Utilisation

### Exemple 1 : Découvrir un Nouveau Projet

1. Créer le projet sur GitHub
2. Exécuter `update-profile.py`
3. Le projet apparaît automatiquement dans `projects-data.json`
4. Exécuter `auto-update-readme.py`
5. Le projet apparaît dans le tableau du README

### Exemple 2 : Mettre à Jour les Métriques

1. `arkalia-metrics-collector` génère `aggregated_metrics.json`
2. Exécuter `update_readme_metrics.py`
3. Les badges et chiffres sont mis à jour dans README

### Exemple 3 : Modifier une Description

1. Modifier la description dans le README du projet
2. Exécuter `update-profile.py`
3. La description est extraite et mise à jour dans `projects-data.json`
4. Exécuter `auto-update-readme.py`
5. Le tableau est mis à jour

---

## ⚠️ Dépannage

### Problème : `projects-data.json` non trouvé

**Solution :**
```bash
python update-profile.py --export config/projects-data.json
```

### Problème : Métriques non mises à jour

**Solution :**
1. Vérifier que `arkalia-metrics-collector` a généré `aggregated_metrics.json`
2. Vérifier le chemin dans `update_readme_metrics.py`
3. Exécuter manuellement : `python scripts/update_readme_metrics.py`

### Problème : Marqueurs non trouvés

**Solution :**
```bash
python auto-update-readme.py --add-markers
```

### Problème : Erreur GitHub API

**Solution :**
1. Vérifier que `GITHUB_TOKEN` est défini
2. Vérifier les limites de rate limit GitHub
3. Attendre quelques minutes et réessayer

---

## 🎯 Améliorations Futures

### Court Terme
- [ ] Génération automatique de la section "Vision Système"
- [ ] Génération automatique des "Featured Projects"
- [ ] Tests automatisés

### Moyen Terme
- [ ] Dashboard de monitoring de l'automatisation
- [ ] Notifications en cas d'erreur
- [ ] Historique des changements

### Long Terme
- [ ] Interface web pour configuration
- [ ] Support multi-organisations
- [ ] Export vers autres plateformes

---

## 📚 Ressources

- **Documentation GitHub API :** https://docs.github.com/en/rest
- **Shields.io Badges :** https://shields.io
- **Markdown Guide :** https://www.markdownguide.org

---

**Dernière mise à jour :** 24 novembre 2025

