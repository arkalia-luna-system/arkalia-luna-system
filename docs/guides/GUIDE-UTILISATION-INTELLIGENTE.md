# 🌙 Guide d'Utilisation Intelligente - Profil GitHub

## 🎯 Objectif

Automatiser complètement la mise à jour de votre profil GitHub pour qu'il reflète toujours l'état réel de vos 11 projets.

---

## 🚀 Workflow Intelligent en 3 Étapes

### **Étape 1 : Découvrir & Analyser** (30 secondes)

```bash
cd /Volumes/T7/github-profile-arkalia
./update.sh
```

**Ce que ça fait :**
- ✅ Récupère tous vos projets depuis GitHub
- ✅ Trouve leurs chemins locaux (Desktop, T7, etc.)
- ✅ Détecte les README automatiquement
- ✅ Génère `projects-data.json` avec toutes les données
- ✅ Génère `README_SECTIONS.md` avec sections prêtes

**Résultat :** 11/11 projets trouvés, 11/11 README détectés

---

### **Étape 2 : Vérifier & Personnaliser** (2 minutes)

```bash
# Voir les données générées
cat projects-data.json | python3 -m json.tool | less

# Voir les sections prêtes
cat README_SECTIONS.md
```

**Ce que vous pouvez faire :**
- ✅ Vérifier que tous les projets sont corrects
- ✅ Personnaliser les descriptions si besoin
- ✅ Ajouter des métriques manquantes
- ✅ Vérifier les chemins locaux

---

### **Étape 3 : Intégrer dans README** (5 minutes)

#### **Option A : Mise à jour Manuelle (Recommandée pour début)**

1. Ouvrez `README_SECTIONS.md`
2. Copiez les sections qui vous intéressent
3. Collez dans votre `README.md` aux bons endroits

**Sections à mettre à jour :**
- 📊 Statistiques globales (ligne ~328)
- 🚀 Tableau des projets (ligne ~212)
- 📦 Liste détaillée (optionnel)

#### **Option B : Mise à jour Automatique (Avancé)**

```bash
python3 auto-update-readme.py
```

Ce script met à jour automatiquement les sections marquées dans votre README.

---

## 📋 Sections à Mettre à Jour dans README.md

### **1. Statistiques Globales** (Ligne ~328)

**Avant :**
```markdown
- **🔢 550+ fichiers Python** (code source uniquement, mesuré)
- **🧪 550+ tests automatisés** (100% CI/CD, mesuré)
- **🎨 196 logos SVG générés** (mesuré)
- **🌍 11 projets actifs** (production + développement)
```

**Après (depuis README_SECTIONS.md) :**
```markdown
- **🔢 11 projets** au total
- **📁 11 projets** trouvés localement
- **📖 11 projets** avec README
- **💻 Langages** : Shell, Python, HTML
```

---

### **2. Tableau des Projets** (Ligne ~212)

**Remplacez le tableau existant par celui généré dans `README_SECTIONS.md`**

Le tableau généré inclut :
- ✅ Tous les projets avec leurs liens GitHub
- ✅ Descriptions à jour
- ✅ Statuts (Local/GitHub only)
- ✅ Langages détectés

---

### **3. Répartition par Langage** (Nouvelle section)

Ajoutez cette section après les statistiques :

```markdown
### **💻 Répartition par Langage**

| Langage | Projets |
|---------|---------|
| Python | 9 |
| Shell | 1 |
| HTML | 1 |
```

---

## 🔄 Workflow Automatisé Quotidien

### **Script Complet** (`update-all.sh`)

Créez ce fichier pour tout automatiser :

```bash
#!/bin/bash
# Mise à jour complète du profil GitHub

cd /Volumes/T7/github-profile-arkalia

echo "🌙 Mise à jour du profil GitHub..."
echo ""

# 1. Découvrir les projets
./update.sh

# 2. Générer les sections
python3 update-profile.py --export config/projects-data.json
python3 auto-update-readme.py

# 3. Afficher un résumé
echo ""
echo "📊 Résumé :"
python3 -c "
import json
data = json.load(open('projects-data.json'))
stats = data['stats']
print(f\"  ✅ {stats['local_projects']}/{stats['total_projects']} projets locaux\")
print(f\"  ✅ {stats['projects_with_readme']} projets avec README\")
print(f\"  ✅ {len(stats['languages'])} langages détectés\")
"

echo ""
echo "✅ Terminé ! Vérifiez README_SECTIONS.md et mettez à jour README.md"
```

**Utilisation :**
```bash
chmod +x update-all.sh
./update-all.sh
```

---

## 🎯 Cas d'Usage Intelligents

### **Cas 1 : Nouveau Projet Ajouté**

1. Créez le projet sur GitHub
2. Clonez-le localement
3. Exécutez `./update.sh`
4. Le nouveau projet apparaît automatiquement dans `projects-data.json`
5. Mettez à jour votre README avec les nouvelles données

---

### **Cas 2 : Projet Déplacé**

Si vous déplacez un projet (ex: de T7 vers Desktop) :

1. Le script le trouve automatiquement grâce à la recherche intelligente
2. Exécutez `./update.sh` pour mettre à jour les chemins
3. Les données sont automatiquement synchronisées

---

### **Cas 3 : Mise à Jour Quotidienne**

**Cron Job (Optionnel) :**

Ajoutez dans votre crontab :
```bash
# Mise à jour quotidienne à 6h du matin
0 6 * * * cd /Volumes/T7/github-profile-arkalia && ./update-all.sh >> /tmp/github-profile-update.log 2>&1
```

---

## 📊 Utilisation des Données JSON

### **Exemple : Extraire les Statistiques**

```python
import json

with open('projects-data.json') as f:
    data = json.load(f)

stats = data['stats']
print(f"Total projets: {stats['total_projects']}")
print(f"Projets locaux: {stats['local_projects']}")
print(f"Langages: {', '.join(stats['languages'].keys())}")
```

### **Exemple : Lister Tous les Projets**

```python
import json

with open('projects-data.json') as f:
    data = json.load(f)

for project in data['projects']:
    print(f"{project['name']}: {project['github_url']}")
    if project.get('local_path'):
        print(f"  📁 Local: {project['local_path']}")
```

---

## 🎨 Personnalisation Avancée

### **Ajouter des Métriques Personnalisées**

Éditez `auto-update-readme.py` pour ajouter :
- Badges personnalisés
- Statistiques calculées
- Graphiques
- Liens spéciaux

### **Filtrer les Projets**

Modifiez `update-profile.py` pour :
- Exclure certains projets
- Grouper par catégorie
- Trier par date/étoiles/langage

---

## 🔧 Dépannage

### **Projet Non Trouvé**

1. Vérifiez qu'il existe sur GitHub
2. Vérifiez qu'il est cloné localement
3. Vérifiez le nom exact (avec/sans underscores/tirets)
4. Ajoutez le chemin dans `update-profile.py` si nécessaire

### **README Non Détecté**

1. Vérifiez qu'un `README.md` existe à la racine
2. Vérifiez les permissions du fichier
3. Vérifiez la casse (README.md vs readme.md)

### **Données Obsolètes**

1. Supprimez `projects-data.json`
2. Ré-exécutez `./update.sh`
3. Vérifiez la date de génération dans le JSON

---

## 📈 Prochaines Étapes

Une fois que vous maîtrisez ce workflow :

1. ✅ **Automatisation GitHub Actions** - Mise à jour quotidienne automatique
2. ✅ **Extraction de métriques** - Depuis les README des projets
3. ✅ **Badges dynamiques** - Génération automatique
4. ✅ **Mise à jour README auto** - Script qui modifie directement README.md

Voir `AMELIORATIONS.md` pour plus de détails.

---

## 💡 Astuces Pro

### **Alias Shell**

Ajoutez dans `~/.zshrc` :
```bash
alias update-profile='cd /Volumes/T7/github-profile-arkalia && ./update-all.sh'
alias view-projects='cd /Volumes/T7/github-profile-arkalia && cat projects-data.json | python3 -m json.tool | less'
```

### **Git Hook (Optionnel)**

Créez `.git/hooks/pre-commit` :
```bash
#!/bin/bash
# Met à jour les données avant chaque commit
cd /Volumes/T7/github-profile-arkalia
./update.sh
git add projects-data.json README_SECTIONS.md
```

---

**🌙 Votre profil GitHub est maintenant intelligent et toujours à jour !**

