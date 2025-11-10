#!/usr/bin/env python3
"""
🎨 Améliorateur Visuel de README
Améliore automatiquement le visuel des README pour tous les projets

Usage:
    python enhance-visual.py [--project PROJECT_NAME] [--all] [--dry-run]
"""

import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class VisualMetrics:
    """Métriques visuelles extraites d'un README"""

    tests: Optional[int] = None
    coverage: Optional[float] = None
    version: Optional[str] = None
    modules: Optional[int] = None
    python_files: Optional[int] = None
    status: str = "production"


class VisualEnhancer:
    """Améliore visuellement les README"""

    def __init__(self):
        self.badge_colors = {
            "production": "25A162",
            "beta": "FFA500",
            "dev": "0078D4",
            "archive": "808080",
            "enterprise": "9F7AEA",
        }

        self.status_emojis = {
            "production": "✅",
            "beta": "🚧",
            "dev": "🔨",
            "archive": "📚",
            "enterprise": "🚀",
        }

    def extract_metrics_from_readme(self, readme_path: Path) -> VisualMetrics:
        """Extrait les métriques visuelles depuis un README"""
        if not readme_path.exists():
            return VisualMetrics()

        content = readme_path.read_text(encoding="utf-8")
        metrics = VisualMetrics()

        # Patterns de recherche
        patterns = {
            "tests": [r"(\d+)\s+test", r"Tests[:\s]+(\d+)", r"🧪\s*(\d+)", r"tests[:\s]+(\d+)"],
            "coverage": [
                r"(\d+(?:\.\d+)?)%\s+coverage",
                r"coverage[:\s]+(\d+(?:\.\d+)?)%",
                r"(\d+(?:\.\d+)?)%\s+couverture",
            ],
            "version": [
                r"v(\d+\.\d+\.\d+)",
                r"version[:\s]+(\d+\.\d+\.\d+)",
                r"VERSION[:\s]+(\d+\.\d+\.\d+)",
            ],
            "modules": [r"(\d+)\s+modules?", r"modules?[:\s]+(\d+)", r"📦\s*(\d+)"],
            "python_files": [
                r"(\d+)\+?\s+fichiers?\s+Python",
                r"(\d+)\+?\s+Python\s+files",
                r"🐍\s*(\d+)",
            ],
        }

        # Extraction
        for metric_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    value = match.group(1)
                    if metric_type == "coverage":
                        metrics.coverage = float(value)
                    elif metric_type in ["tests", "modules", "python_files"]:
                        setattr(metrics, metric_type, int(value))
                    elif metric_type == "version":
                        metrics.version = value
                    break

        # Détection du statut
        status_patterns = {
            "production": r"✅\s+Production|Production-ready|✅\s+prod",
            "beta": r"🚧\s+Beta|Beta|🚧",
            "dev": r"🔨\s+Dev|Development|En développement",
            "archive": r"📚\s+Archive|Archive",
            "enterprise": r"🚀\s+Enterprise|Enterprise|🏢",
        }

        for status, pattern in status_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                metrics.status = status
                break

        return metrics

    def generate_badge(
        self, label: str, value: str, color: str = "blue", style: str = "for-the-badge"
    ) -> str:
        """Génère un badge shields.io"""
        # Nettoie les valeurs pour l'URL
        label_clean = label.replace(" ", "%20")
        value_clean = str(value).replace(" ", "%20").replace("+", "%2B")

        return f"[![{label}](https://img.shields.io/badge/{label_clean}-{value_clean}-{color}?style={style}&logo={label.lower()}&logoColor=white)](https://github.com/arkalia-luna-system)"

    def generate_enhanced_badges(self, metrics: VisualMetrics, project_name: str) -> str:
        """Génère des badges améliorés pour un projet"""
        badges = []

        # Badge version
        if metrics.version:
            color = "25A162" if metrics.status == "production" else "0078D4"
            badges.append(self.generate_badge("VERSION", metrics.version, color))

        # Badge tests
        if metrics.tests:
            badges.append(self.generate_badge("TESTS", f"{metrics.tests}_pass", "25A162"))

        # Badge coverage
        if metrics.coverage:
            color = (
                "25A162"
                if metrics.coverage >= 70
                else "FFA500" if metrics.coverage >= 50 else "FF6B6B"
            )
            badges.append(self.generate_badge("COVERAGE", f"{metrics.coverage}%", color))

        # Badge modules
        if metrics.modules:
            badges.append(self.generate_badge("MODULES", f"{metrics.modules}", "3776AB"))

        # Badge status
        status_color = self.badge_colors.get(metrics.status, "0078D4")
        status_label = metrics.status.upper()
        badges.append(self.generate_badge("STATUS", status_label, status_color))

        return " ".join(badges)

    def generate_project_card(
        self, project_name: str, description: str, github_url: str, metrics: VisualMetrics
    ) -> str:
        """Génère une carte visuelle pour un projet"""
        emoji = self.status_emojis.get(metrics.status, "📦")
        badges = self.generate_enhanced_badges(metrics, project_name)

        card = f"""
<div align="center">

### {emoji} **{project_name}**

**{description}**

{badges}

[🚀 Découvrir]({github_url}) • [📚 Documentation]({github_url}#readme)

</div>
"""
        return card.strip()

    def enhance_projects_table(self, projects_data: List[Dict[str, Any]]) -> str:
        """Améliore le tableau des projets avec des métriques visuelles"""
        lines = [
            "| | Projet | Description | Stack | Métriques | Status |",
            "|---|--------|-------------|-------|-----------|---------|",
        ]

        for project in projects_data:
            name = project["name"]
            github_url = project["github_url"]
            description = project.get("description", "")[:80]
            language = project.get("language", "N/A")

            # Cherche le README local pour extraire les métriques
            readme_path = None
            if project.get("readme_path"):
                readme_path = Path(project["readme_path"])

            metrics = VisualMetrics()
            if readme_path and readme_path.exists():
                metrics = self.extract_metrics_from_readme(readme_path)

            # Emoji selon le type de projet
            emoji = self._get_project_emoji(name)

            # Métriques formatées
            metrics_str = []
            if metrics.tests:
                metrics_str.append(f"🧪 {metrics.tests} tests")
            if metrics.coverage:
                metrics_str.append(f"📊 {metrics.coverage}%")
            if metrics.modules:
                metrics_str.append(f"📦 {metrics.modules} modules")

            metrics_display = " • ".join(metrics_str) if metrics_str else "N/A"

            # Status avec emoji
            status_emoji = self.status_emojis.get(metrics.status, "📦")
            status_display = f"{status_emoji} {metrics.status.title()}"

            # Version si disponible
            version_badge = ""
            if metrics.version:
                version_badge = f"<br/>v{metrics.version}"

            lines.append(
                f"| {emoji} | **[{name}]({github_url})**{version_badge} | "
                f"{description} | {language} | {metrics_display} | {status_display} |"
            )

        return "\n".join(lines)

    def _get_project_emoji(self, project_name: str) -> str:
        """Retourne l'emoji approprié pour un projet"""
        name_lower = project_name.lower()

        emoji_map = {
            "bbia": "🤖",
            "quest": "🎮",
            "logo": "🎨",
            "branding": "🎨",
            "cia": "📱",
            "aria": "🧠",
            "luna-pro": "🌕",
            "pipeline": "🔧",
            "athalia": "🔧",
            "metrics": "📊",
            "template": "⚙️",
            "nours": "📚",
        }

        for key, emoji in emoji_map.items():
            if key in name_lower:
                return emoji

        return "📦"

    def enhance_readme_section(
        self, readme_path: Path, section_marker: str, new_content: str, dry_run: bool = False
    ) -> bool:
        """Met à jour une section spécifique du README"""
        if not readme_path.exists():
            print(f"⚠️  README non trouvé : {readme_path}")
            return False

        content = readme_path.read_text(encoding="utf-8")

        # Cherche le marqueur de section
        pattern = f"(<!-- AUTO-UPDATE:{section_marker} -->)(.*?)(<!-- END-AUTO-UPDATE:{section_marker} -->)"

        if re.search(pattern, content, re.DOTALL):
            # Remplace le contenu entre les marqueurs
            new_content_full = f"<!-- AUTO-UPDATE:{section_marker} -->\n{new_content}\n<!-- END-AUTO-UPDATE:{section_marker} -->"
            content = re.sub(pattern, new_content_full, content, flags=re.DOTALL)

            if not dry_run:
                readme_path.write_text(content, encoding="utf-8")
                print(f"✅ Section '{section_marker}' mise à jour dans {readme_path.name}")
            else:
                print(f"🔍 [DRY-RUN] Section '{section_marker}' serait mise à jour")
            return True
        else:
            print(f"⚠️  Marqueur 'AUTO-UPDATE:{section_marker}' non trouvé dans {readme_path.name}")
            return False

    def generate_visual_stats_section(self, stats: Dict[str, Any]) -> str:
        """Génère une section de statistiques visuelles"""
        lines = [
            "### **📈 Statistiques Visuelles**",
            "",
            '<div align="center">',
            "",
            "| Métrique | Valeur | Progression |",
            "|----------|--------|-------------|",
        ]

        # Calcule les progressions (exemple)
        total_projects = stats.get("total_projects", 0)
        local_projects = stats.get("local_projects", 0)
        projects_with_readme = stats.get("projects_with_readme", 0)

        def progress_bar(value: int, max_value: int) -> str:
            """Génère une barre de progression ASCII"""
            percentage = int((value / max_value) * 100) if max_value > 0 else 0
            filled = int(percentage / 10)
            return "█" * filled + "░" * (10 - filled) + f" {percentage}%"

        lines.append(
            f"| 📦 **Projets Totaux** | {total_projects} | {progress_bar(total_projects, 20)} |"
        )
        lines.append(
            f"| 📁 **Projets Locaux** | {local_projects} | {progress_bar(local_projects, total_projects)} |"
        )
        lines.append(
            f"| 📖 **Avec README** | {projects_with_readme} | {progress_bar(projects_with_readme, total_projects)} |"
        )

        if stats.get("total_stars", 0) > 0:
            lines.append(
                f"| ⭐ **Stars Totales** | {stats['total_stars']} | {progress_bar(stats['total_stars'], 100)} |"
            )

        lines.extend(["", "</div>", ""])

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="🎨 Améliorateur Visuel de README")
    parser.add_argument("--project", type=str, help="Nom du projet à améliorer (optionnel)")
    parser.add_argument("--all", action="store_true", help="Améliore tous les projets")
    parser.add_argument("--dry-run", action="store_true", help="Mode test (ne modifie rien)")
    parser.add_argument(
        "--data",
        type=str,
        default="projects-data.json",
        help="Fichier JSON des projets (défaut: projects-data.json)",
    )

    args = parser.parse_args()

    script_dir = Path(__file__).parent
    data_file = script_dir / args.data

    if not data_file.exists():
        print(f"❌ Fichier non trouvé : {data_file}")
        print("💡 Exécutez d'abord : python update-profile.py")
        return 1

    print("🎨 Améliorateur Visuel de README")
    print("=" * 60)

    # Charge les données
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    enhancer = VisualEnhancer()
    projects = data.get("projects", [])

    if args.project:
        # Améliore un projet spécifique
        project = next((p for p in projects if p["name"] == args.project), None)
        if not project:
            print(f"❌ Projet '{args.project}' non trouvé")
            return 1

        if project.get("readme_path"):
            readme_path = Path(project["readme_path"])
            metrics = enhancer.extract_metrics_from_readme(readme_path)
            print(f"\n📊 Métriques extraites pour {args.project}:")
            print(f"   - Tests: {metrics.tests}")
            print(f"   - Coverage: {metrics.coverage}%")
            print(f"   - Version: {metrics.version}")
            print(f"   - Modules: {metrics.modules}")
            print(f"   - Status: {metrics.status}")

            # Génère les badges
            badges = enhancer.generate_enhanced_badges(metrics, args.project)
            print(f"\n🎨 Badges générés:\n{badges}")
        else:
            print(f"⚠️  Pas de README trouvé pour {args.project}")

    elif args.all:
        # Améliore tous les projets
        print(f"\n🔍 Analyse de {len(projects)} projets...\n")

        for project in projects:
            name = project["name"]
            if project.get("readme_path"):
                readme_path = Path(project["readme_path"])
                metrics = enhancer.extract_metrics_from_readme(readme_path)
                print(
                    f"✅ {name}: {metrics.tests} tests, {metrics.coverage}% coverage, v{metrics.version}"
                )
            else:
                print(f"⚠️  {name}: Pas de README local")

        # Génère le tableau amélioré
        print("\n📊 Génération du tableau amélioré...")
        enhanced_table = enhancer.enhance_projects_table(projects)

        # Sauvegarde dans un fichier
        output_file = script_dir / "ENHANCED_PROJECTS_TABLE.md"
        output_file.write_text(enhanced_table, encoding="utf-8")
        print(f"✅ Tableau amélioré sauvegardé : {output_file}")

        # Génère les stats visuelles
        stats_section = enhancer.generate_visual_stats_section(data.get("stats", {}))
        stats_file = script_dir / "ENHANCED_STATS.md"
        stats_file.write_text(stats_section, encoding="utf-8")
        print(f"✅ Stats visuelles sauvegardées : {stats_file}")

    else:
        print("💡 Utilisez --project NOM ou --all")
        return 1

    print("\n✅ Terminé !")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
