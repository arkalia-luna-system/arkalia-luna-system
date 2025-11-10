#!/usr/bin/env python3
"""
🔍 Analyseur et Optimiseur de README
Détecte les doublons, automatise les sections, optimise la taille

Usage:
    python optimize-readme.py [--dry-run] [--analyze-only]
"""

import re
import json
import argparse
from pathlib import Path
from typing import Dict, List
from collections import Counter


class ReadmeOptimizer:
    """Analyse et optimise le README"""

    def __init__(self, readme_path: Path):
        self.readme_path = readme_path
        self.content = readme_path.read_text(encoding="utf-8")
        self.issues = []
        self.optimizations = []

    def analyze_duplicates(self) -> List[Dict]:
        """Détecte les sections dupliquées"""
        duplicates = []

        # Détecte les titres dupliqués
        title_pattern = r"^#+\s+\*\*([^*]+)\*\*"
        titles = []
        for match in re.finditer(title_pattern, self.content, re.MULTILINE):
            title = match.group(1).strip()
            line_num = self.content[: match.start()].count("\n") + 1
            titles.append((title, line_num))

        title_counts = Counter([t[0] for t in titles])
        for title, count in title_counts.items():
            if count > 1:
                lines = [line for title_text, line in titles if title_text == title]
                duplicates.append(
                    {"type": "titre_dupliqué", "title": title, "count": count, "lines": lines}
                )

        # Détecte les sections hero dupliquées
        hero_pattern = r'<div align="center">.*?#\s+\*\*Arkalia Luna System\*\*.*?</div>'
        hero_matches = list(re.finditer(hero_pattern, self.content, re.DOTALL))
        if len(hero_matches) > 1:
            lines = [self.content[: m.start()].count("\n") + 1 for m in hero_matches]
            duplicates.append(
                {"type": "hero_section_dupliquée", "count": len(hero_matches), "lines": lines}
            )

        # Détecte les badges dupliqués
        badge_pattern = r"\[!\[([^\]]+)\]\([^\)]+\)\]"
        badges = []
        for match in re.finditer(badge_pattern, self.content):
            badge_text = match.group(1)
            line_num = self.content[: match.start()].count("\n") + 1
            badges.append((badge_text, line_num))

        badge_counts = Counter([b[0] for b in badges])
        for badge, count in badge_counts.items():
            if count > 1 and count > 2:  # Plus de 2 occurrences
                lines = [line for badge_text, line in badges if badge_text == badge]
                duplicates.append(
                    {
                        "type": "badge_dupliqué",
                        "badge": badge,
                        "count": count,
                        "lines": lines[:5],  # Limite à 5 pour l'affichage
                    }
                )

        return duplicates

    def analyze_manual_sections(self) -> List[Dict]:
        """Détecte les sections qui pourraient être automatisées"""
        manual_sections = []

        # Tableau des projets (ligne ~212)
        projects_table_pattern = r"\|\s*\|\s*Projet\s*\|\s*Description"
        if re.search(projects_table_pattern, self.content):
            match = re.search(projects_table_pattern, self.content)
            line = self.content[: match.start()].count("\n") + 1
            manual_sections.append(
                {
                    "type": "tableau_projets",
                    "line": line,
                    "suggestion": "Automatiser avec generate-readme-sections.py",
                }
            )

        # Métriques hardcodées
        hardcoded_metrics = [
            (r"550\+\s+fichiers?\s+Python", "Fichiers Python"),
            (r"550\+\s+tests?", "Tests"),
            (r"196\s+logos?", "Logos SVG"),
        ]

        for pattern, metric_name in hardcoded_metrics:
            if re.search(pattern, self.content, re.IGNORECASE):
                match = re.search(pattern, self.content, re.IGNORECASE)
                line = self.content[: match.start()].count("\n") + 1
                manual_sections.append(
                    {
                        "type": "métrique_hardcodée",
                        "metric": metric_name,
                        "line": line,
                        "suggestion": "Extraire depuis projects-data.json",
                    }
                )

        return manual_sections

    def analyze_size_issues(self) -> List[Dict]:
        """Analyse les problèmes de taille"""
        issues = []

        # Compte les images
        img_pattern = r"<img[^>]+>"
        images = list(re.finditer(img_pattern, self.content))
        if len(images) > 20:
            issues.append(
                {
                    "type": "trop_d_images",
                    "count": len(images),
                    "suggestion": "Réduire ou utiliser lazy loading",
                }
            )

        # Compte les emojis inline
        emoji_pattern = r'<img[^>]+width="(?:14|16|18|20)"[^>]*>'
        emoji_imgs = list(re.finditer(emoji_pattern, self.content))
        if len(emoji_imgs) > 30:
            issues.append(
                {
                    "type": "trop_d_emojis_inline",
                    "count": len(emoji_imgs),
                    "suggestion": "Réduire les emojis inline répétitifs",
                }
            )

        # Taille du fichier
        file_size = len(self.content)
        if file_size > 50000:  # > 50KB
            issues.append(
                {
                    "type": "fichier_trop_lourd",
                    "size_kb": round(file_size / 1024, 1),
                    "suggestion": "Optimiser et supprimer les doublons",
                }
            )

        return issues

    def remove_duplicates(self) -> str:
        """Supprime les doublons détectés"""
        content = self.content

        # Supprime la deuxième hero section
        hero_pattern = r'(<div align="center">.*?#\s+\*\*Arkalia Luna System\*\*.*?</div>)'
        matches = list(re.finditer(hero_pattern, content, re.DOTALL))
        if len(matches) > 1:
            # Garde la première, supprime les autres
            for match in reversed(matches[1:]):
                content = content[: match.start()] + content[match.end() :]
                self.optimizations.append("Hero section dupliquée supprimée")

        return content

    def optimize_images(self) -> str:
        """Optimise les images (lazy loading, taille)"""
        content = self.content

        # Ajoute loading="lazy" aux images qui n'en ont pas
        img_pattern = r"(<img[^>]+)(?<!loading=)(>)"

        def add_lazy(match):
            img_tag = match.group(1)
            if "loading=" not in img_tag:
                return img_tag + ' loading="lazy"' + match.group(2)
            return match.group(0)

        content = re.sub(img_pattern, add_lazy, content)

        return content

    def generate_automated_sections(self, data_file: Path) -> Dict[str, str]:
        """Génère les sections automatisées depuis projects-data.json"""
        if not data_file.exists():
            return {}

        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        stats = data.get("stats", {})
        projects = data.get("projects", [])

        sections = {}

        # Section stats automatisée
        stats_section = f"""### **📈 Statistiques Globales**

- **🔢 {stats.get('total_projects', 0)} projets** au total
- **📁 {stats.get('local_projects', 0)} projets** trouvés localement
- **📖 {stats.get('projects_with_readme', 0)} projets** avec README
- **⭐ {stats.get('total_stars', 0)} stars** totales

"""

        if stats.get("languages"):
            languages = ", ".join(stats["languages"].keys())
            stats_section += f"- **💻 Langages** : {languages}\n\n"

        stats_section += f"*Dernière mise à jour automatique : {stats.get('last_updated', 'N/A')}*"

        sections["stats"] = stats_section

        # Tableau projets automatisé (simplifié)
        table_lines = [
            "| | Projet | Description | Stack | Status |",
            "|---|--------|-------------|-------|--------|",
        ]

        for project in projects[:11]:  # Limite à 11
            name = project["name"]
            url = project["github_url"]
            desc = (project.get("description") or "")[:60]
            lang = project.get("language", "N/A")
            status = "✅" if project.get("local_path") else "🌐"

            # Emoji simple
            emoji = "🤖" if "bbia" in name.lower() else "📦"

            table_lines.append(f"| {emoji} | **[{name}]({url})** | {desc}... | {lang} | {status} |")

        sections["projects_table"] = "\n".join(table_lines)

        return sections

    def analyze(self) -> Dict:
        """Analyse complète du README"""
        return {
            "duplicates": self.analyze_duplicates(),
            "manual_sections": self.analyze_manual_sections(),
            "size_issues": self.analyze_size_issues(),
            "file_size_kb": round(len(self.content) / 1024, 1),
            "line_count": self.content.count("\n"),
        }

    def optimize(self, data_file: Path, dry_run: bool = False) -> str:
        """Optimise le README"""
        content = self.content

        # 1. Supprime les doublons
        content = self.remove_duplicates()

        # 2. Optimise les images
        content = self.optimize_images()

        # 3. Génère les sections automatisées
        sections = self.generate_automated_sections(data_file)

        # 4. Remplace les sections marquées
        for section_name, new_content in sections.items():
            pattern = rf"(<!--\s*AUTO-UPDATE:{section_name}\s*-->)(.*?)(<!--\s*END-AUTO-UPDATE:{section_name}\s*-->)"
            replacement = f"<!-- AUTO-UPDATE:{section_name} -->\n{new_content}\n<!-- END-AUTO-UPDATE:{section_name} -->"

            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                self.optimizations.append(f"Section {section_name} automatisée")
            else:
                # Ajoute le marqueur si absent
                if section_name == "stats":
                    stats_pattern = r"(###\s+\*\*📈\s+Statistiques\s+Globales\*\*)"
                    if re.search(stats_pattern, content):
                        content = re.sub(
                            stats_pattern, f"<!-- AUTO-UPDATE:{section_name} -->\n\\1", content
                        )
                        # Ajoute le marqueur de fin
                        content = re.sub(
                            r"(###\s+\*\*💻\s+.*Langage)",
                            f"<!-- END-AUTO-UPDATE:{section_name} -->\n\\1",
                            content,
                            count=1,
                        )

        if not dry_run:
            self.readme_path.write_text(content, encoding="utf-8")

        return content


def main():
    parser = argparse.ArgumentParser(description="🔍 Analyseur et Optimiseur de README")
    parser.add_argument("--dry-run", action="store_true", help="Mode test")
    parser.add_argument("--analyze-only", action="store_true", help="Analyse uniquement")
    parser.add_argument("--readme", type=str, default="README.md", help="Fichier README")

    args = parser.parse_args()

    script_dir = Path(__file__).parent
    readme_path = script_dir / args.readme
    data_file = script_dir / "projects-data.json"

    if not readme_path.exists():
        print(f"❌ README non trouvé : {readme_path}")
        return 1

    optimizer = ReadmeOptimizer(readme_path)

    print("🔍 Analyse du README...")
    print("=" * 60)

    analysis = optimizer.analyze()

    # Affiche les résultats
    print(f"\n📊 Taille : {analysis['file_size_kb']} KB ({analysis['line_count']} lignes)")

    if analysis["duplicates"]:
        print(f"\n⚠️  {len(analysis['duplicates'])} doublon(s) détecté(s) :")
        for dup in analysis["duplicates"]:
            print(
                f"   - {dup['type']} : {dup.get('count', 'N/A')} occurrences (lignes {dup.get('lines', [])[:3]})"
            )

    if analysis["manual_sections"]:
        print(f"\n📝 {len(analysis['manual_sections'])} section(s) manuelle(s) détectée(s) :")
        for section in analysis["manual_sections"]:
            print(f"   - {section['type']} (ligne {section.get('line', 'N/A')})")
            print(f"     💡 {section.get('suggestion', '')}")

    if analysis["size_issues"]:
        print(f"\n⚡ {len(analysis['size_issues'])} problème(s) de taille :")
        for issue in analysis["size_issues"]:
            print(f"   - {issue['type']} : {issue.get('count', issue.get('size_kb', 'N/A'))}")
            print(f"     💡 {issue.get('suggestion', '')}")

    if args.analyze_only:
        return 0

    print("\n🔧 Optimisation...")
    print("=" * 60)

    optimized = optimizer.optimize(data_file, dry_run=args.dry_run)

    if optimizer.optimizations:
        print("\n✅ Optimisations appliquées :")
        for opt in optimizer.optimizations:
            print(f"   - {opt}")

    if args.dry_run:
        print("\n🔍 Mode DRY-RUN : Aucune modification effectuée")
    else:
        print(f"\n✅ README optimisé : {readme_path}")
        print(f"   Nouvelle taille : {round(len(optimized) / 1024, 1)} KB")

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
