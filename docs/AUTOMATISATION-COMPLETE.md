# 🌙 Documentation Complète - Automatisation du Profil GitHub

**Date** : 24 novembre 2025  
**Version** : 2.0

---

## 🎯 Vue d'Ensemble

Ce projet automatise complètement la mise à jour de votre profil GitHub. Tous les scripts, workflows et processus sont documentés ici.

---

## 📁 Structure des Scripts

### Scripts Principaux

#### 1. `update-profile.py`
**Rôle** : Découvre tous les projets GitHub et génère `config/projects-data.json`

**Usage** :
```bash
python update-profile.py [--verbose] [--export config/projects-data.json]
```

**Fonctionnalités** :
- ✅ Récupère tous les repos GitHub via API
- ✅ Cherche les chemins locaux intelligemment
- ✅ Extrait les descriptions depuis les README
- ✅ Détecte les langages principaux et secondaires
- ✅ Génère `config/projects-data.json` avec toutes les données

**Options** :
- `--verbose` : Mode verbeux
- `--export FILE` : Fichier de sortie (défaut: `config/projects-data.json`)
- `--base-path PATH` : Chemin de base pour chercher les projets (défaut: `/Volumes/T7`)

---

#### 2. `auto-update-readme.py`
**Rôle** : Met à jour automatiquement les sections marquées dans `README.md`

**Usage** :
```bash
python auto-update-readme.py [--dry-run] [--add-markers]
```

**Fonctionnalités** :
- ✅ Met à jour la section statistiques (`<!-- AUTO-UPDATE:stats -->`)
- ✅ Met à jour le tableau des projets (`<!-- AUTO-UPDATE:projects -->`)
- ✅ Génère automatiquement les colonnes Rôle/Stack/Status
- ✅ Dates dynamiques en français

**Options** :
- `--dry-run` : Mode test (ne modifie rien)
- `--add-markers` : Ajoute les marqueurs si absents
- `--readme FILE` : Fichier README à mettre à jour (défaut: `README.md`)

**Marqueurs supportés** :
- `<!-- AUTO-UPDATE:stats -->` : Section statistiques
- `<!-- AUTO-UPDATE:projects -->` : Tableau des projets
- `<!-- AUTO-UPDATE:languages -->` : Section langages (optionnel)

---

#### 3. `scripts/audit-projects.py`
**Rôle** : Audite la qualité de tous les projets

**Usage** :
```bash
python scripts/audit-projects.py [--output FILE] [--verbose]
```

**Fonctionnalités** :
- ✅ Audit du README (titre, description, badges, sections)
- ✅ Audit de la structure (tests, docs, CI/CD, Docker)
- ✅ Audit des métriques (tests, coverage, version)
- ✅ Audit de la cohérence (nommage, description, langage)
- ✅ Génère un rapport Markdown avec scores et recommandations

**Options** :
- `--output FILE` : Fichier de sortie (défaut: `audits/AUDIT-COMPLET-PROJETS.md`)
- `--verbose` : Mode verbeux
- `--data FILE` : Fichier de données (défaut: `config/projects-data.json`)

---

#### 4. `scripts/update_readme_metrics.py`
**Rôle** : Met à jour les métriques depuis `arkalia-metrics-collector`

**Usage** :
```bash
python scripts/update_readme_metrics.py
```

**Fonctionnalités** :
- ✅ Lit `aggregated_metrics.json` depuis `arkalia-metrics-collector`
- ✅ Met à jour les badges et chiffres dans README
- ✅ Dates dynamiques en français

**Prérequis** :
- Le projet `arkalia-metrics-collector` doit être cloné ou accessible
- Le fichier `aggregated_metrics.json` doit exister

---

#### 5. `scripts/create_badges_metrics.py`
**Rôle** : Génère les badges de métriques

**Usage** :
```bash
python scripts/create_badges_metrics.py
```

**Fonctionnalités** :
- ✅ Génère les badges depuis les métriques agrégées
- ✅ Met à jour les badges dans README

---

#### 6. `scripts/update-all.sh`
**Rôle** : Script qui fait tout en une fois

**Usage** :
```bash
./scripts/update-all.sh
```

**Fonctionnalités** :
1. Découvre les projets (`update-profile.py`)
2. Met à jour le README (`auto-update-readme.py`)
3. Lance l'audit (`scripts/audit-projects.py`)

**Résultat** :
- `config/projects-data.json` mis à jour
- `README.md` mis à jour
- `audits/AUDIT-COMPLET-PROJETS.md` généré

---

## 🔄 Workflows GitHub Actions

### 1. `.github/workflows/update-profile.yml`
**Rôle** : Mise à jour automatique du profil (hebdomadaire)

**Déclenchement** :
- Tous les dimanches à 2h UTC
- Manuellement via `workflow_dispatch`

**Actions** :
1. Découvre les projets
2. Met à jour le README
3. Commit et push automatique

---

### 2. `.github/workflows/update-metrics.yml`
**Rôle** : Mise à jour automatique des métriques (quotidienne)

**Déclenchement** :
- Tous les jours à 2h UTC
- Manuellement via `workflow_dispatch`

**Actions** :
1. Checkout `arkalia-metrics-collector`
2. Exécute l'agrégation des métriques
3. Met à jour les métriques dans README
4. Crée les badges
5. Commit et push automatique

---

### 3. `.github/workflows/update-complete.yml` ⭐ **NOUVEAU**
**Rôle** : Mise à jour complète (hebdomadaire)

**Déclenchement** :
- Tous les dimanches à 3h UTC
- Manuellement via `workflow_dispatch`

**Actions** :
1. Découvre les projets
2. Met à jour le README
3. Audite les projets
4. Met à jour les métriques
5. Crée les badges
6. Commit et push automatique

**Avantage** : Tout en un seul workflow

---

### 4. `.github/workflows/ci.yml`
**Rôle** : Lint et tests (sur push)

**Déclenchement** :
- Sur chaque push
- Sur les pull requests

**Actions** :
1. Lint Python (ruff, black)
2. Tests (si présents)

---

## 🚀 Workflow Complet Recommandé

### Workflow Manuel (Local)

```bash
# 1. Mise à jour complète
cd /Volumes/T7/github-profile-arkalia
./scripts/update-all.sh

# 2. Vérifier les changements
git status
git diff README.md

# 3. Commit et push
git add .
git commit -m "🌙 Mise à jour automatique"
git push
```

### Workflow Automatique (GitHub Actions)

Les workflows GitHub Actions s'exécutent automatiquement :
- **Quotidien** : `update-metrics.yml` (métriques)
- **Hebdomadaire** : `update-profile.yml` (profil) + `update-complete.yml` (tout)

---

## 📊 Fichiers Générés

### `config/projects-data.json`
**Généré par** : `update-profile.py`

**Contenu** :
- Liste de tous les projets GitHub
- Chemins locaux (si trouvés)
- Descriptions
- Langages
- Stars
- Dates de génération

---

### `audits/AUDIT-COMPLET-PROJETS.md`
**Généré par** : `scripts/audit-projects.py`

**Contenu** :
- Score global pour chaque projet
- Points forts
- Points à améliorer
- Recommandations

---

### `metrics/aggregated_metrics.json`
**Généré par** : `arkalia-metrics-collector`

**Contenu** :
- Métriques agrégées de tous les projets
- Modules, lignes, tests, coverage
- Évolution temporelle

---

## 🔧 Configuration

### Variables d'Environnement

- `GITHUB_TOKEN` : Token GitHub pour l'API (optionnel mais recommandé)

### Fichiers de Configuration

- `config/projects-data.json` : Données des projets
- `requirements.txt` : Dépendances Python
- `.github/workflows/*.yml` : Workflows GitHub Actions

---

## 🐛 Dépannage

### Problème : Projets non trouvés localement

**Solution** :
1. Vérifier les chemins dans `update-profile.py`
2. Ajouter manuellement dans `config/projects-data.json`
3. Utiliser `--base-path` pour spécifier un chemin différent

---

### Problème : README non mis à jour

**Solution** :
1. Vérifier que les marqueurs `<!-- AUTO-UPDATE:... -->` sont présents
2. Utiliser `--add-markers` pour les ajouter automatiquement
3. Vérifier les permissions d'écriture

---

### Problème : Métriques non mises à jour

**Solution** :
1. Vérifier que `arkalia-metrics-collector` est accessible
2. Vérifier que `aggregated_metrics.json` existe
3. Vérifier les logs du workflow GitHub Actions

---

## 📝 Bonnes Pratiques

1. **Exécuter régulièrement** : `./scripts/update-all.sh` au moins une fois par semaine
2. **Vérifier les audits** : Consulter `audits/AUDIT-COMPLET-PROJETS.md` pour voir les améliorations possibles
3. **Commit les changements** : Toujours commit les mises à jour automatiques
4. **Documenter les modifications** : Si vous modifiez manuellement le README, documentez pourquoi

---

## 🎯 Prochaines Améliorations

- [ ] Génération automatique de la section "Vision Système"
- [ ] Génération automatique des "Featured Projects"
- [ ] Tests automatisés pour les scripts
- [ ] Dashboard de monitoring de l'automatisation

---

**Dernière mise à jour** : 24 novembre 2025

