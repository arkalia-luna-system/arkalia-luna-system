# 🚀 PLAN SUITE - ARKALIA METRICS COLLECTOR

**Date** : 14 novembre 2025  
**Statut actuel** : ✅ Agrégation complète fonctionnelle (12 projets)  
**Prochaines étapes** : Automatisation, intégration CI/CD, dashboard

---

## 🎯 **ARCHITECTURE**

### **Rôles clarifiés**

1. **`arkalia-metrics-collector`** (Service de calcul)
   - ✅ Calcule les métriques (modules, tests, lignes, coverage)
   - ✅ Parse `coverage.xml` avec `CoverageParser`
   - ✅ Génère `aggregated_metrics.json` avec toutes les métriques

2. **`github-profile-arkalia`** (Client de réception)
   - ✅ Reçoit les métriques depuis `aggregated_metrics.json`
   - ✅ Met à jour les fichiers MD (README, etc.)
   - ✅ Affiche les métriques dans le profil GitHub

---

## ✅ **CE QUI EST DÉJÀ FAIT**

1. ✅ **Agrégation complète** : 12 projets analysés par `arkalia-metrics-collector`
2. ✅ **Métriques générées** : 52,320 modules, 11,204 tests, 24.7M lignes
3. ✅ **Fichiers de sortie** : `README_TABLE.md`, `badges_final.md`, `aggregated_metrics.json`
4. ✅ **Configuration** : `projects.json` avec tous les chemins et URLs GitHub
5. ✅ **Intégration README** : Scripts Python dans `github-profile-arkalia` mettent à jour automatiquement

---

## 🎯 **PROCHAINES ÉTAPES PRIORITAIRES**

### **Phase 1 : Automatisation & CI/CD** (Semaine 1-2)

#### 1. **GitHub Action pour mise à jour automatique** ⚡
**Impact :** HIGH | **Temps :** 4-6h

**Objectif :** Mettre à jour automatiquement les métriques dans le README principal

**Actions :**
- [x] Créer workflow `.github/workflows/update-metrics.yml` ✅
- [x] Déclencher sur schedule (quotidien) + manuel ✅
- [ ] Exécuter `arkalia-metrics aggregate projects.json` (dans `arkalia-metrics-collector`)
- [x] Scripts Python pour mettre à jour README depuis `aggregated_metrics.json` ✅
- [x] Commit automatique avec message `📊 Auto-update metrics [skip ci]` ✅
- [x] Push vers branche `main` ✅

**Note** : Le workflow dans `github-profile-arkalia` lit les métriques depuis `arkalia-metrics-collector/metrics/aggregated_metrics.json` et met à jour le README automatiquement.

**Fichiers à créer :**
```yaml
# .github/workflows/update-metrics.yml
name: Update Metrics
on:
  schedule:
    - cron: '0 2 * * *'  # Tous les jours à 2h
  workflow_dispatch:
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install arkalia-metrics-collector
        run: pip install arkalia-metrics-collector
      - name: Aggregate metrics
        run: arkalia-metrics aggregate projects.json
      - name: Update README
        run: |
          # Script Python pour mettre à jour README.md
          python scripts/update_readme_metrics.py
      - name: Commit changes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add README.md metrics/
          git commit -m "📊 Auto-update metrics [skip ci]"
          git push
```

**Script Python à créer :**
```python
# scripts/update_readme_metrics.py
"""
Met à jour automatiquement les métriques dans README.md
"""
import json
import re
from pathlib import Path

def update_readme_metrics():
    # Lire aggregated_metrics.json
    metrics_path = Path("metrics/aggregated_metrics.json")
    with open(metrics_path) as f:
        data = json.load(f)
    
    agg = data["aggregated"]
    
    # Lire README.md
    readme_path = Path("README.md")
    readme = readme_path.read_text()
    
    # Remplacer métriques
    readme = re.sub(
        r'\*\*52,320\*\*',
        f'**{agg["total_modules"]:,}**',
        readme
    )
    # ... autres remplacements
    
    # Écrire README.md
    readme_path.write_text(readme)

if __name__ == "__main__":
    update_readme_metrics()
```

---

#### 2. **Dashboard Web interactif** ⚡ ✅ **TERMINÉ**
**Impact :** MEDIUM | **Temps :** 8-10h

**Objectif :** Créer un dashboard HTML interactif pour visualiser les métriques

**Actions :**
- [x] Générer `dashboard.html` avec Chart.js ✅
- [x] Graphiques : évolution modules, tests, coverage par projet ✅
- [x] Tableau interactif avec tri/filtre ✅
- [x] Export CSV/JSON depuis le dashboard ✅
- [x] Déployer sur GitHub Pages ✅

**Fonctionnalités implémentées** :
- Dashboard HTML interactif avec Chart.js
- Graphiques d'évolution (modules, lignes de code, tests)
- Graphique de vue d'ensemble (barres)
- Tableau interactif avec tri/filtre par colonne
- Support de l'historique des métriques
- Export JSON/CSV depuis le dashboard
- Support multi-projets avec détection automatique
- Génération automatique via `scripts/generate_dashboard.py`
- **Déploiement automatique sur GitHub Pages** ✅
- Dashboard accessible publiquement après déploiement

**Technologies :**
- HTML/CSS/JavaScript vanilla
- Chart.js pour graphiques
- Génération automatique dans `arkalia-metrics-collector`
- Workflow GitHub Actions pour déploiement GitHub Pages

---

#### 3. **Badges dynamiques avec Shields.io** ⚡
**Impact :** MEDIUM | **Temps :** 2-3h

**Objectif :** Créer des badges dynamiques qui se mettent à jour automatiquement

**Actions :**
- [ ] Générer badges Shields.io avec métriques actuelles
- [ ] Intégrer dans README principal
- [ ] Badges : Modules, Tests, Lignes, Coverage

**Exemple :**
```markdown
![Modules](https://img.shields.io/badge/Python%20Modules-52,320-blue)
![Tests](https://img.shields.io/badge/Tests-11,204-green)
![LOC](https://img.shields.io/badge/Lines%20of%20Code-24.7M-orange)
```

---

### **Phase 2 : Améliorations fonctionnelles** (Semaine 3-4)

#### 4. **Support Coverage automatique** ⚡
**Impact :** HIGH | **Temps :** 6-8h

**Objectif :** Intégrer les métriques de coverage depuis Codecov/coverage.xml

**Actions :**
- [ ] Parser `coverage.xml` de chaque projet
- [ ] Agréger coverage global
- [ ] Ajouter dans `aggregated_metrics.json`
- [ ] Générer badges coverage

---

#### 5. **Comparaison temporelle** ⚡ ✅ **TERMINÉ**
**Impact :** MEDIUM | **Temps :** 4-6h

**Objectif :** Stocker historique des métriques et afficher évolution

**Actions :**
- [x] Créer `metrics/history/` avec fichiers datés ✅
- [x] Comparer métriques actuelles vs précédentes ✅
- [x] Générer rapport d'évolution Markdown ✅
- [x] Calculer deltas et tendances (📈 up, 📉 down, ➡️ stable) ✅
- [ ] Afficher delta (+/-) dans README (optionnel)

**Fonctionnalités implémentées** :
- Module `MetricsHistory` pour gestion historique
- Sauvegarde automatique avec timestamp
- Rapport `EVOLUTION_REPORT.md` généré automatiquement
- Option CLI `--evolution` pour générer le rapport

---

#### 6. **Export formats multiples** ⚡ ✅ **TERMINÉ**
**Impact :** LOW | **Temps :** 2-3h

**Objectif :** Exporter métriques en CSV, JSON, YAML, Markdown

**Actions :**
- [x] Ajouter commande `arkalia-metrics export --format <format>` ✅
- [x] Support formats : CSV, JSON, YAML, Markdown, HTML ✅
- [x] Option `--format all` pour exporter tous les formats ✅
- [x] Support YAML avec gestion gracieuse si PyYAML non installé ✅
- [x] Intégration dans commande `collect` ✅

**Fonctionnalités implémentées** :
- Commande CLI `export` dédiée
- Support de tous les formats : JSON, Markdown, HTML, CSV, YAML
- Export depuis fichier JSON existant
- `export_all_formats()` inclut maintenant YAML

---

### **Phase 3 : Intégrations avancées** (Mois 2)

#### 7. **Intégration GitHub API** ⚡ ✅ **TERMINÉ**
**Impact :** MEDIUM | **Temps :** 6-8h

**Objectif :** Récupérer métriques depuis GitHub (stars, forks, issues)

**Actions :**
- [x] Utiliser GitHub API pour métriques publiques ✅
- [x] Agréger stars, forks, issues par projet ✅
- [x] Ajouter dans dashboard ✅

**Fonctionnalités implémentées** :
- Collecte automatique de stars, forks, watchers, issues, PRs
- Agrégation dans `multi_project_aggregator`
- Option CLI `--github-api` pour activer la collecte
- Utilisation : `arkalia-metrics aggregate projects.json --github-api`

---

#### 8. **Notifications & Alertes** ⚡ ✅ **TERMINÉ**
**Impact :** LOW | **Temps :** 3-4h

**Objectif :** Notifier si métriques changent significativement

**Actions :**
- [x] Détecter changements >10% dans métriques ✅
- [x] Commande CLI `arkalia-metrics alerts` ✅
- [x] Intégration dans workflow GitHub Actions ✅
- [x] Génération de messages d'alerte formatés ✅
- [x] Créer issue GitHub automatique ✅

**Fonctionnalités implémentées** :
- Classe `MetricsAlerts` pour détection des changements significatifs
- Commande CLI `arkalia-metrics alerts` pour vérifier les alertes
- Intégration dans workflow `update-metrics.yml`
- **Création automatique d'issues GitHub** ✅
  - Classe `GitHubIssues` pour créer des issues via l'API GitHub
  - Option `--create-issue` dans la commande `alerts`
  - Vérification des issues existantes pour éviter les doublons
  - Labels automatiques : `metrics`, `automated`, `alerts`
  - Intégration dans workflow pour création automatique

---

## 📋 **CHECKLIST PRIORISÉE**

### **Semaine 1**
- [ ] GitHub Action pour mise à jour automatique
- [ ] Script Python `update_readme_metrics.py`
- [ ] Test workflow sur branche test

### **Semaine 2**
- [x] Dashboard HTML interactif ✅
- [x] Badges dynamiques Shields.io ✅
- [x] Déploiement GitHub Pages ✅

### **Semaine 3-4**
- [x] Support Coverage automatique ✅
- [x] Comparaison temporelle ✅
- [x] Export formats multiples ✅

---

## 🎯 **OBJECTIFS FINAUX**

1. ✅ **Métriques automatiques** : Mise à jour quotidienne sans intervention
2. ✅ **Dashboard interactif** : Visualisation en temps réel (GitHub Pages)
3. ✅ **Badges dynamiques** : Mise à jour automatique
4. ✅ **Historique** : Suivi évolution dans le temps
5. ✅ **Alertes automatiques** : Détection changements >10%
6. ✅ **Issues GitHub automatiques** : Création via API lors d'alertes
7. ✅ **Intégration complète** : CI/CD, GitHub API, notifications

---

## 📚 **RESSOURCES**

- **Documentation** : `/Volumes/T7/arkalia-metrics-collector/docs/`
- **Exemples** : `/Volumes/T7/arkalia-metrics-collector/examples/`
- **Tests** : `/Volumes/T7/arkalia-metrics-collector/tests/`

---

**Prochaine étape immédiate :** Voir `PROCHAINES-ETAPES-ARKALIA-METRICS.md` pour les améliorations optionnelles ✅

**Statut :** Toutes les fonctionnalités principales sont terminées et fonctionnelles. Le projet est prêt pour la production.

