# 🔍 **GUIDE : DÉCOUVRIR LES PROBLÈMES DANS TES PROJETS**

**Comment identifier les problèmes et incohérences dans tes projets GitHub**

---

## 🎯 **OBJECTIF**

Ce guide t'aide à découvrir systématiquement les problèmes dans tes projets GitHub pour les corriger et améliorer ton profil.

---

## 📋 **MÉTHODE DE DÉCOUVERTE**

### **1. Vérifier les métriques**

**Problèmes courants :**
- ❌ Métriques non sourcées (ex: "550+ modules" sans lien de vérification)
- ❌ Métriques incohérentes entre différents fichiers
- ❌ Métriques obsolètes (non mises à jour)
- ❌ Métriques exagérées ou imprécises

**Comment vérifier :**
```bash
# Vérifier les métriques dans le README
grep -i "modules\|tests\|lignes" README.md

# Comparer avec les métriques réelles
cd /Volumes/T7/arkalia-metrics-collector
arkalia-metrics aggregate projects.json
```

**Solution :** Utiliser `arkalia-metrics-collector` pour automatiser les métriques

---

### **2. Vérifier les liens**

**Problèmes courants :**
- ❌ Liens cassés (404)
- ❌ Liens vers des repos privés ou inexistants
- ❌ Liens vers des branches qui n'existent plus
- ❌ Liens vers des fichiers déplacés

**Comment vérifier :**
```bash
# Extraire tous les liens du README
grep -oP 'https?://[^\s\)]+' README.md

# Tester chaque lien manuellement ou avec un script
```

**Solution :** Utiliser un outil de vérification de liens (ex: `linkchecker`)

---

### **3. Vérifier la cohérence**

**Problèmes courants :**
- ❌ Descriptions différentes du même projet dans plusieurs fichiers
- ❌ Dates incohérentes (ex: "dernière mise à jour" différente)
- ❌ Statuts contradictoires (ex: "Production" vs "Beta")
- ❌ Métriques différentes dans différents fichiers

**Comment vérifier :**
```bash
# Chercher les mentions d'un projet
grep -r "arkalia-luna-pro" .

# Comparer les descriptions
grep -r "description\|Description" README.md
```

**Solution :** Centraliser les informations dans un fichier unique (ex: `config/projects-data.json`)

---

### **4. Vérifier la documentation**

**Problèmes courants :**
- ❌ README incomplet ou obsolète
- ❌ Sections manquantes (Installation, Usage, Contributing)
- ❌ Exemples de code non fonctionnels
- ❌ Documentation non synchronisée avec le code

**Comment vérifier :**
```bash
# Vérifier la présence des sections essentielles
grep -E "## (Installation|Usage|Contributing|License)" README.md

# Vérifier la longueur du README
wc -l README.md
```

**Solution :** Utiliser un template de README et vérifier régulièrement

---

### **5. Vérifier les badges**

**Problèmes courants :**
- ❌ Badges cassés (images non chargées)
- ❌ Badges avec métriques incorrectes
- ❌ Badges manquants (coverage, tests, etc.)
- ❌ Badges non mis à jour

**Comment vérifier :**
```bash
# Extraire tous les badges
grep -oP 'https://img\.shields\.io/[^\]]+' README.md

# Vérifier visuellement dans le navigateur
```

**Solution :** Utiliser `scripts/create_badges_metrics.py` pour générer les badges

---

### **6. Vérifier le code**

**Problèmes courants :**
- ❌ Code non formaté (Black, Ruff)
- ❌ Erreurs de linting
- ❌ Tests qui échouent
- ❌ Code non typé (type hints manquants)

**Comment vérifier :**
```bash
# Vérifier le formatage
black --check .

# Vérifier le linting
ruff check .

# Vérifier les tests
pytest
```

**Solution :** Configurer CI/CD pour vérifier automatiquement

---

## 🔧 **OUTILS RECOMMANDÉS**

### **Pour les métriques**
- **`arkalia-metrics-collector`** → Calcule automatiquement les métriques
- **`scripts/update_readme_metrics.py`** → Met à jour le README avec les métriques

### **Pour les liens**
- **`linkchecker`** → Vérifie les liens cassés
- **`wget --spider`** → Teste les liens individuellement

### **Pour la cohérence**
- **`grep -r`** → Cherche les occurrences dans tous les fichiers
- **`diff`** → Compare les fichiers

### **Pour la documentation**
- **`markdownlint`** → Vérifie le formatage Markdown
- **`vale`** → Vérifie le style de la documentation

---

## 📊 **CHECKLIST RAPIDE**

Avant de considérer un projet comme "cohérent", vérifie :

- [ ] Toutes les métriques sont sourcées et vérifiables
- [ ] Tous les liens fonctionnent
- [ ] Les descriptions sont cohérentes partout
- [ ] La documentation est complète et à jour
- [ ] Tous les badges fonctionnent
- [ ] Le code est formaté et sans erreurs
- [ ] Les tests passent
- [ ] Le README est professionnel et complet

---

## 🚀 **PROCHAINES ÉTAPES**

1. **Découvre un problème** → Utilise cette checklist
2. **Audite avec Perplexity** → Utilise `prompts/PROMPT-AUDIT-PERPLEXITY.md`
3. **Trouve une solution** → Consulte `guides/GUIDE-SOLUTIONS-METRIQUES.md`
4. **Planifie l'action** → Consulte `plans/PLAN-ACTION-1-MOIS.md`
5. **Vérifie le résultat** → Consulte `statut/STATUT.md`

---

**Ce guide t'aide à maintenir un profil GitHub professionnel et cohérent.** ✅

