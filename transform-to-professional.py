#!/usr/bin/env python3
"""
🌙 Transformateur de Profil GitHub avec Couleurs BBIA Branding
Transforme le README avec les couleurs officielles BBIA (#008181)

Usage:
    python transform-to-professional.py [--dry-run] [--backup]
"""

import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple
import argparse


class ProfessionalTransformer:
    """Transforme le README en version professionnelle"""

    def __init__(self):
        # Thème BBIA Branding (couleurs officielles du projet BBIA)
        # Couleurs extraites de: https://github.com/arkalia-luna-system/bbia_branding
        # BBIA Blue: #008181 (RGB(0, 129, 129)) - Couleur principale
        self.theme_config = {
            "github_stats": "dark",  # Thème sombre avec couleurs BBIA
            "streak": "dark",  # Thème sombre
            "activity": "dark",  # Thème sombre
            "trophy": "dark",  # Thème sombre
            "title_color": "008181",  # BBIA Blue (sans #)
            "icon_color": "008181",  # BBIA Blue
            "ring_color": "008181",  # BBIA Blue
            "fire_color": "008181",  # BBIA Blue
            "line_color": "008181",  # BBIA Blue
            "point_color": "008181",  # BBIA Blue
        }

        # Couleurs de badges BBIA (basées sur la palette officielle)
        self.badge_colors = {
            "production": "238636",  # Vert GitHub (succès)
            "beta": "9E6A03",  # Orange (attention)
            "dev": "008181",  # BBIA Blue (développement)
            "archive": "6E7681",  # Gris (archive)
            "enterprise": "008181",  # BBIA Blue (enterprise)
            "organization": "008181",  # BBIA Blue (couleur principale)
            "projects": "008181",  # BBIA Blue
            "version": "008181",  # BBIA Blue
            "stack": "008181",  # BBIA Blue
        }

    def transform_github_stats(self, content: str) -> str:
        """Transforme les URLs GitHub Stats vers thème BBIA (couleurs officielles)"""
        # Remplace tokyonight par dark avec couleurs BBIA Blue (#008181)
        patterns = [
            (r'theme=tokyonight', 'theme=dark'),
            (r'theme=tokyo-night', 'theme=dark'),
            (r'title_color=58A6FF', f'title_color={self.theme_config["title_color"]}'),
            (r'icon_color=58A6FF', f'icon_color={self.theme_config["icon_color"]}'),
            (r'ring=58A6FF', f'ring={self.theme_config["ring_color"]}'),
            (r'fire=58A6FF', f'fire={self.theme_config["fire_color"]}'),
            (r'currStreakLabel=58A6FF', f'currStreakLabel={self.theme_config["fire_color"]}'),
            (r'color=58A6FF', f'color={self.theme_config["line_color"]}'),
            (r'line=58A6FF', f'line={self.theme_config["line_color"]}'),
            (r'point=58A6FF', f'point={self.theme_config["point_color"]}'),
        ]

        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        return content

    def transform_badges(self, content: str) -> str:
        """Transforme les badges avec les couleurs BBIA officielles"""
        # Remplace les badges avec les couleurs BBIA Blue (#008181)
        badge_replacements = [
            (r'badge/Organization-Arkalia%20Luna%20System-blue', 
             f'badge/Organization-Arkalia%20Luna%20System-{self.badge_colors["organization"]}'),
            (r'badge/Stack-Python.*?-blue', 
             f'badge/Stack-Python%20%7C%20Flask%20%7C%20FastAPI%20%7C%20Docker-{self.badge_colors["stack"]}'),
            (r'badge/AI-Cognitive.*?-purple', 
             f'badge/AI-Cognitive%20Engines%20%7C%20Emotions%20%7C%20LUNA-{self.badge_colors["dev"]}'),
            (r'badge/VERSION-([^-]+)-0078D4',  # Badge BBIA Version existant
             f'badge/VERSION-\\1-{self.badge_colors["version"]}'),
        ]

        for pattern, replacement in badge_replacements:
            content = re.sub(pattern, replacement, content)

        return content

    def simplify_emojis(self, content: str) -> str:
        """Réduit les emojis inline excessifs"""
        # Garde les emojis dans les titres et premières colonnes
        # Supprime les emojis inline répétitifs dans le texte
        
        # Pattern: emoji en fin de ligne après texte
        content = re.sub(
            r'<img src="https://raw\.githubusercontent\.com/arkalia-luna-system/arkalia-luna-logo/main/exports/screenshots/[^"]+" width="(?:14|16|18|20)"[^>]*>\s*\n',
            '\n',
            content
        )
        
        # Garde les emojis dans les tableaux (première colonne)
        # Garde les emojis dans les titres
        
        return content

    def reorganize_sections(self, content: str) -> str:
        """Réorganise les sections pour structure professionnelle"""
        # L'ordre actuel est déjà bon, on va juste améliorer
        
        # Supprime les sections redondantes si nécessaire
        # Améliore les séparateurs
        
        return content

    def improve_hero_section(self, content: str) -> str:
        """Améliore la section hero (en-tête)"""
        # Simplifie l'en-tête
        # Centre mieux les éléments
        
        # Remplace les 2 logos par un seul centré plus grand
        hero_pattern = r'<div align="center">\s*<img src="[^"]+"[^>]+width="120"[^>]+>.*?</div>'
        
        new_hero = '''<div align="center">

<img src="https://raw.githubusercontent.com/arkalia-luna-system/arkalia-luna-logo/main/exports/screenshots/ultimate-power-200.svg" alt="Arkalia Luna System" width="140" height="140" style="border-radius: 16px; box-shadow: 0 8px 16px rgba(0, 129, 129, 0.3);" title="Arkalia Luna System - Écosystème IA & Robotique">

# 🌙 **Arkalia Luna System**

**Autodidacte depuis février 2025 • 11 projets en production • IA • Robotique • Design • DevOps**

**`"Apprendre vite, coder mieux, partager tout."`** 🚀

</div>'''
        
        # Remplace si le pattern existe
        if re.search(hero_pattern, content, re.DOTALL):
            content = re.sub(hero_pattern, new_hero, content, flags=re.DOTALL)
        
        return content

    def transform_readme(self, readme_path: Path, dry_run: bool = False) -> Tuple[str, Dict]:
        """Transforme le README complet"""
        if not readme_path.exists():
            raise FileNotFoundError(f"README non trouvé : {readme_path}")

        content = readme_path.read_text(encoding="utf-8")
        original_content = content
        changes = {}

        # 1. Transforme GitHub Stats
        content = self.transform_github_stats(content)
        if content != original_content:
            changes["github_stats"] = "Thème changé: tokyonight → dark avec couleurs BBIA (#008181)"

        # 2. Transforme les badges
        content = self.transform_badges(content)
        if content != original_content:
            changes["badges"] = "Badges mis à jour avec couleurs BBIA (#008181)"

        # 3. Améliore hero section
        content = self.improve_hero_section(content)
        if content != original_content:
            changes["hero"] = "Hero section simplifiée avec ombre BBIA Blue"

        # 4. Simplifie emojis (optionnel, peut être trop agressif)
        # content = self.simplify_emojis(content)

        # 5. Réorganise sections
        content = self.reorganize_sections(content)

        if not dry_run:
            readme_path.write_text(content, encoding="utf-8")
            changes["saved"] = f"Fichier sauvegardé : {readme_path}"

        return content, changes

    def create_github_structure(self, base_path: Path, dry_run: bool = False):
        """Crée la structure .github/ pour projet professionnel"""
        github_dir = base_path / ".github"
        workflows_dir = github_dir / "workflows"
        issue_template_dir = github_dir / "ISSUE_TEMPLATE"

        if not dry_run:
            workflows_dir.mkdir(parents=True, exist_ok=True)
            issue_template_dir.mkdir(parents=True, exist_ok=True)

        # Workflow CI/CD
        workflow_content = """name: Update Profile

on:
  schedule:
    - cron: '0 0 * * 0'  # Toutes les semaines
  workflow_dispatch:  # Manuel

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install requests
      - name: Update profile
        run: python scripts/update-profile.py
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add projects-data.json
          git commit -m "chore: update profile data" || exit 0
          git push
"""

        workflow_file = workflows_dir / "update-profile.yml"
        if not dry_run:
            workflow_file.write_text(workflow_content, encoding="utf-8")
            print(f"✅ Créé : {workflow_file}")

        # Template d'issue
        issue_template = """---
name: Feature Request
about: Proposer une amélioration
title: '[FEATURE] '
labels: enhancement
---

## Description
<!-- Décrivez votre proposition -->

## Motivation
<!-- Pourquoi cette fonctionnalité serait utile ? -->

## Solution proposée
<!-- Comment voyez-vous cette fonctionnalité ? -->
"""

        issue_file = issue_template_dir / "feature_request.md"
        if not dry_run:
            issue_file.write_text(issue_template, encoding="utf-8")
            print(f"✅ Créé : {issue_file}")

        return {
            "workflow": str(workflow_file),
            "issue_template": str(issue_file),
        }


def main():
    parser = argparse.ArgumentParser(
        description="🌙 Transformateur de Profil GitHub avec Couleurs BBIA Branding"
    )
    parser.add_argument("--dry-run", action="store_true", help="Mode test (ne modifie rien)")
    parser.add_argument("--backup", action="store_true", help="Crée une sauvegarde avant modification")
    parser.add_argument(
        "--readme",
        type=str,
        default="README.md",
        help="Chemin vers README.md (défaut: README.md)",
    )

    args = parser.parse_args()

    script_dir = Path(__file__).parent
    readme_path = script_dir / args.readme

    print("🌙 Transformateur de Profil GitHub - Couleurs BBIA Branding")
    print("=" * 60)
    print("🎨 Couleurs officielles BBIA: #008181 (BBIA Blue)")
    print(f"📁 README : {readme_path}")
    print(f"🔍 Mode : {'DRY-RUN (test)' if args.dry_run else 'TRANSFORMATION'}")
    print()

    if not readme_path.exists():
        print(f"❌ README non trouvé : {readme_path}")
        return 1

    # Sauvegarde si demandé
    if args.backup and not args.dry_run:
        backup_path = readme_path.with_suffix(f".backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
        shutil.copy2(readme_path, backup_path)
        print(f"💾 Sauvegarde créée : {backup_path}")
        print()

    transformer = ProfessionalTransformer()

    # Transforme le README
    print("🔄 Transformation du README avec les couleurs BBIA...")
    print("   🎨 Couleur principale: #008181 (BBIA Blue)")
    try:
        content, changes = transformer.transform_readme(readme_path, dry_run=args.dry_run)
        print()
        print("📊 Changements effectués :")
        for key, value in changes.items():
            print(f"   ✅ {key}: {value}")
        print()

        # Crée la structure .github/
        print("📁 Création de la structure .github/...")
        structure = transformer.create_github_structure(script_dir, dry_run=args.dry_run)
        print()

        if args.dry_run:
            print("🔍 Mode DRY-RUN : Aucune modification effectuée")
            print("💡 Supprimez --dry-run pour appliquer les changements")
        else:
            print("✅ Transformation terminée !")
            print()
            print("📋 Prochaines étapes :")
            print("   1. Vérifiez le README.md transformé")
            print("   2. Testez les nouveaux thèmes GitHub Stats")
            print("   3. Commit et push les changements")
            print("   4. La structure .github/ est prête pour CI/CD")

    except Exception as e:
        print(f"❌ Erreur : {e}")
        return 1

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

