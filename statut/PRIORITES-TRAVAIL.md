# 🎯 PRIORITÉS DE TRAVAIL - 2025-11-24

**Objectif** : Atteindre 9.5/10 (niveau avancé)  
**Note actuelle** : 8.3/10  
**Deadline** : 1 mois

---

## 🔴 **URGENT - À FAIRE EN PREMIER (Semaine 1)**

### **1. Projet : `arkalia-metrics-collector`** ⚡
**Impact** : CRITIQUE | **Temps** : 4-6h | **Priorité** : #1 | **Statut** : ✅ **TERMINÉ**

**Pourquoi** : C'est la base pour automatiser toutes les métriques du profil principal.

**Architecture** :
- **`arkalia-metrics-collector`** : Calcule les métriques et génère `aggregated_metrics.json`
- **`github-profile-arkalia`** : Lit `aggregated_metrics.json` et met à jour les MD automatiquement

**Actions concrètes** :
1. ✅ **Étendre le collecteur pour GitHub API** (2-3h) — **TERMINÉ**
   - ✅ Scraper GitHub API pour métriques (stars, forks, last update)
   - ✅ Calculer coverage global depuis tous les projets
   - ✅ Compter modules Python automatiquement (exclure `__pycache__`, tests, etc.)
   - ⚠️ Compter SVG générés (Luna Logo + BBIA Branding) — À ajouter si nécessaire

2. ✅ **Générer tableau récap automatique** (1-2h) — **TERMINÉ**
   - ✅ Script qui génère le tableau récap des projets pour README principal
   - ✅ Format : `projet | statut | tests | coverage | last update | prod tag`
   - ✅ Export Markdown prêt à copier-coller

3. ✅ **Générer badges automatiques** (1h) — **TERMINÉ**
   - ✅ Badges Shields.io pour métriques
   - ✅ Badges Codecov pour coverage
   - ✅ Badges "last release" pour chaque projet

**Fichiers créés** :
- ✅ `github_collector.py` — Collecteur GitHub API
- ✅ `multi_project_aggregator.py` — Agrégateur multi-projets
- ✅ `badges_generator.py` — Générateur de badges
- ✅ CLI étendu avec nouvelles commandes
- ✅ Documentation mise à jour

**Résultat** :
- ✅ Script Python qui génère automatiquement toutes les métriques
- ✅ Tableau récap à jour dans README principal (via CLI)
- ✅ Métriques sourcées et vérifiables

---

### **2. Projet : Profil principal (`github-profile-arkalia`)** ⚡
**Impact** : CRITIQUE | **Temps** : 2-3h | **Priorité** : #2

**Pourquoi** : C'est la première chose que les recruteurs voient.

**Actions concrètes** :
1. **Ajouter sommaire Markdown cliquable** (30 min)
   - En tête du README.md principal
   - Utiliser `[TOC]` auto ou créer manuellement
   - Sections : Featured Projects, Autres Projets, Impact & Performance, etc.

2. **Remplacer métriques statiques par métriques sourcées** (1-2h)
   - Utiliser les scripts de `arkalia-metrics-collector`
   - Remplacer "550+ modules" → `[X modules](lien-inventaire)`
   - Remplacer "~64% coverage" → `[X% coverage](lien-codecov)`
   - Remplacer "196 SVG" → `[X SVG](lien-inventaire)`

3. **Améliorer About GitHub (SEO)** (30 min)
   - Condenser à <160 caractères
   - Intégrer mots-clés : "AI, Python, DevOps, Robotics, Healthcare"
   - Exemple : "AI/ML engineer | Python, FastAPI, Docker | Robotics & Healthcare | Open Source"

**Résultat attendu** :
- README avec sommaire cliquable
- Métriques sourcées et vérifiables
- About GitHub optimisé SEO

---

### **3. Projets : Configurer Codecov (6 projets)** ⚡
**Impact** : CRITIQUE | **Temps** : 2-3h | **Priorité** : #3

**Pourquoi** : Coverage non vérifiable publiquement = perte de crédibilité.

**Projets concernés** :
- ❌ Luna Logo (151 tests, 78% coverage) - **À FAIRE**
- ❌ Quest (179 tests) - **À FAIRE**
- ❌ Luna Pro (671 tests, 59% coverage) - **À FAIRE**
- ✅ **CIA** - **TERMINÉ** (Codecov configuré Python + Flutter, 61 tests, 66% coverage fichiers testés, 10.69% global)
- ✅ Metrics Collector - **TERMINÉ** (Codecov configuré + SEO optimisé)
- ❌ Base Template - **À FAIRE**

**Actions par projet** (20-30 min/projet) :
1. Configurer Codecov dans GitHub Actions
2. Ajouter badge Codecov dans README
3. Vérifier que le badge s'affiche correctement
4. Documenter la source de la métrique coverage

**Résultat attendu** :
- Badge Codecov visible sur chaque README
- Coverage vérifiable publiquement
- Liens vers rapports coverage fonctionnels

---

## 🟠 **HAUTE PRIORITÉ - Semaine 2**

### **4. Projet : README principaux (Featured Projects)** 
**Impact** : HAUT | **Temps** : 3-4h | **Priorité** : #4

**Projets concernés** :
- Luna Pro (README principal)
- BBIA Sim (README principal)
- BBIA Branding (README principal)

**Actions concrètes** :
1. **Ajouter sommaire Markdown cliquable** (30 min/projet)
2. **Ajouter screenshots/GIF onboarding** (1h/projet)
   - Screenshots dashboard (Grafana, Docker, Prometheus)
   - GIF démo rapide (30s)
   - Images compressées, alt text
3. **Ajouter section FAQ/troubleshooting** (30 min/projet)
   - Erreurs typiques + solutions
   - Edge cases documentés

**Résultat attendu** :
- README avec sommaire, screenshots, FAQ
- UX améliorée pour contributeurs

---

### **5. Projet : About GitHub (tous les projets)**
**Impact** : HAUT | **Temps** : 1-2h | **Priorité** : #5

**Actions concrètes** :
- Refactorer tous les About pour <160 caractères
- Intégrer 3-4 mots-clés stratégiques par projet
- Optimiser SEO GitHub

**Résultat attendu** :
- About optimisés SEO sur tous les projets
- Découvrabilité améliorée

---

## 🟡 **MOYENNE PRIORITÉ - Semaine 3-4**

### **6. Projet : Documentation (tous les projets)**
**Impact** : MOYEN | **Temps** : 2-3h | **Priorité** : #6

**Actions concrètes** :
- Uniformiser docstrings (Google style) sur modules publics
- Ajouter guide contribution plus haut dans README
- Ajouter section "benchmarks performances"

**Résultat attendu** :
- Documentation uniforme et professionnelle
- Onboarding contributeurs amélioré

---

## 📊 **RÉSUMÉ PAR ORDRE DE PRIORITÉ**

### **Cette semaine (Semaine 1)** :

1. **`arkalia-metrics-collector`** (4-6h)
   - Étendre pour GitHub API
   - Générer tableau récap automatique
   - Générer badges automatiques

2. **Profil principal** (2-3h)
   - Ajouter sommaire Markdown
   - Remplacer métriques statiques par sourcées
   - Améliorer About GitHub SEO

3. **Codecov (4 projets restants)** (1.5-2h)
   - Luna Logo, Quest, Luna Pro, Base Template
   - ✅ Metrics Collector déjà fait
   - ✅ CIA déjà fait (Python + Flutter)

**Total Semaine 1** : 8-12h

---

### **Semaine 2** :

4. **README Featured Projects** (3-4h)
   - Sommaires, screenshots, FAQ

5. **About GitHub (tous projets)** (1-2h)
   - SEO <160 caractères

**Total Semaine 2** : 4-6h

---

### **Semaine 3-4** :

6. **Documentation uniforme** (2-3h)
   - Docstrings, guides contribution, benchmarks

**Total Semaine 3-4** : 2-3h

---

## 🎯 **RECOMMANDATION FINALE**

**✅ TERMINÉ** : `arkalia-metrics-collector` (4-6h) — **COMPLET**

**Prochaines étapes** :
1. **Tester les fonctionnalités** (30 min) — Voir `PROCHAINES-ETAPES-METRICS.md`
2. **Générer tableau récap pour README** (1h)
3. **Mettre à jour métriques README principal** (1h)
4. **Configurer Codecov** (1.5-2h) — 4 projets restants (CIA terminé ✅)

**Total restant pour atteindre 9.5/10** : 4-4.5h

---

## ✅ **NOUVEAU : Metrics Collector - Codecov & SEO terminés**

**Date** : 14 novembre 2025

### **Codecov configuré** ✅
- Fichier `.codecov.yml` créé avec seuil 80%
- Documentation : `docs/CODECOV_SETUP.md`
- Branches suivies : `main` et `develop`

### **SEO optimisé** ✅
- README optimisé avec mots-clés
- `pyproject.toml` optimisé (description, keywords, classifiers)
- Guide SEO : `docs/SEO_GUIDE.md`

### **À faire manuellement sur GitHub** :
1. Settings > General > About → Description courte
2. Topics → `python`, `metrics`, `code-analysis`, `test-coverage`, `codecov`, `ci-cd`, etc.

---

**Date de création** : 2025-11-24  
**Date de mise à jour** : 2025-11-24  
**Statut** : ✅ Étape 1 terminée, prêt pour étape 2

