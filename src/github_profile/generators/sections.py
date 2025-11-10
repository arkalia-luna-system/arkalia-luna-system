#!/usr/bin/env python3
"""
🌙 Générateur Automatique de Sections README
Génère des sections markdown à partir de projects-data.json

Usage:
    python -m github_profile.generators.sections [--output README_SECTIONS.md]
    ou après installation: generate-sections [--output README_SECTIONS.md]
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


def load_projects_data(data_file: Path) -> Dict[str, Any]:
    """Charge les données des projets"""
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_projects_table(projects: List[Dict[str, Any]]) -> str:
    """Génère un tableau markdown des projets"""
    lines = [
        "| | Projet | Description | Stack | Métriques | Status |",
        "|---|--------|-------------|-------|-----------|---------|",
    ]

    # Emojis par type de projet
    project_emojis = {
        "bbia": "🤖",
        "quest": "🎮",
        "logo": "🎨",
        "branding": "🎨",
        "cia": "📱",
        "aria": "🧠",
        "luna-pro": "🌕",
        "pipeline": "🔧",
        "metrics": "📊",
        "template": "⚙️",
        "nours": "📚",
    }

    for project in projects:
        name = project["name"]
        github_url = project["github_url"]
        description = project.get("description", "") or "Projet en développement"
        language = project.get("language", "N/A")
        local_path = project.get("local_path")
        readme_path = project.get("readme_path")

        # Détermine l'emoji
        emoji = "📦"
        name_lower = name.lower()
        for key, emoji_val in project_emojis.items():
            if key in name_lower:
                emoji = emoji_val
                break

        # Status
        if local_path and readme_path:
            status = "✅ Local"
        elif local_path:
            status = "⚠️ Pas de README"
        else:
            status = "🌐 GitHub only"

        # Stack simplifié
        stack = language or "N/A"

        # Métriques basiques
        metrics = f"📁 {language}" if language else "N/A"

        # Ligne du tableau
        lines.append(
            f"| {emoji} | **[{name}]({github_url})** | "
            f"{description[:80]}{'...' if len(description) > 80 else ''} | "
            f"{stack} | {metrics} | {status} |"
        )

    return "\n".join(lines)


def generate_stats_section(stats: Dict[str, Any]) -> str:
    """Génère la section statistiques"""
    lines = [
        "### **📈 Statistiques Globales**",
        "",
        f"- **🔢 {stats['total_projects']} projets** au total",
        f"- **📁 {stats['local_projects']} projets** trouvés localement",
        f"- **📖 {stats['projects_with_readme']} projets** avec README",
        f"- **⭐ {stats['total_stars']} stars** totales",
        "",
    ]

    if stats.get("languages"):
        languages = ", ".join(stats["languages"].keys())
        lines.append(f"- **💻 Langages** : {languages}")
        lines.append("")

    lines.append(f"*Dernière mise à jour : {stats.get('last_updated', 'N/A')}*")

    return "\n".join(lines)


def generate_languages_breakdown(stats: Dict[str, Any]) -> str:
    """Génère la répartition par langage"""
    if not stats.get("languages"):
        return ""

    lines = [
        "### **💻 Répartition par Langage**",
        "",
        "| Langage | Projets |",
        "|---------|---------|",
    ]

    for lang, count in sorted(stats["languages"].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {lang} | {count} |")

    return "\n".join(lines)


def generate_projects_list(projects: List[Dict[str, Any]]) -> str:
    """Génère une liste simple des projets"""
    lines = ["### **📦 Liste des Projets**", ""]

    for i, project in enumerate(projects, 1):
        name = project["name"]
        github_url = project["github_url"]
        description = project.get("description", "")
        local_path = project.get("local_path")

        status_icon = "✅" if local_path else "🌐"
        lines.append(f"{i}. {status_icon} **[{name}]({github_url})**")
        if description:
            lines.append(f"   - {description[:100]}{'...' if len(description) > 100 else ''}")
        if local_path:
            lines.append(f"   - 📁 Local: `{local_path}`")
        lines.append("")

    return "\n".join(lines)


def generate_readme_sections(data: Dict[str, Any], output_file: Path):
    """Génère toutes les sections README"""
    projects = data.get("projects", [])
    stats = data.get("stats", {})

    sections = []

    # En-tête
    sections.append("# 📊 Sections Générées Automatiquement")
    sections.append("")
    sections.append(f"*Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    sections.append("")
    sections.append("---")
    sections.append("")

    # Statistiques
    sections.append(generate_stats_section(stats))
    sections.append("")

    # Répartition par langage
    lang_section = generate_languages_breakdown(stats)
    if lang_section:
        sections.append(lang_section)
        sections.append("")

    # Tableau des projets
    sections.append("## 🚀 **Projets Phares**")
    sections.append("")
    sections.append(generate_projects_table(projects))
    sections.append("")

    # Liste détaillée
    sections.append("---")
    sections.append("")
    sections.append(generate_projects_list(projects))

    # Écrit le fichier
    content = "\n".join(sections)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Sections générées : {output_file}")
    print(f"   - {len(projects)} projets")
    print(f"   - {len(sections)} sections")


def main():
    parser = argparse.ArgumentParser(
        description="🌙 Générateur de sections README depuis projects-data.json"
    )
    parser.add_argument(
        "--data",
        type=str,
        default="projects-data.json",
        help="Fichier JSON des projets (défaut: projects-data.json)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="README_SECTIONS.md",
        help="Fichier de sortie (défaut: README_SECTIONS.md)",
    )

    args = parser.parse_args()

    # Trouve la racine du projet
    script_dir = Path(__file__).parent.parent.parent

    # Gère les chemins relatifs et absolus
    if args.data == "projects-data.json":
        data_file = script_dir / "config" / "projects-data.json"
    elif Path(args.data).is_absolute():
        data_file = Path(args.data)
    else:
        data_file = script_dir / args.data

    if args.output == "README_SECTIONS.md":
        output_file = script_dir / "docs" / "README_SECTIONS.md"
    elif Path(args.output).is_absolute():
        output_file = Path(args.output)
    else:
        output_file = script_dir / args.output

    if not data_file.exists():
        print(f"❌ Fichier non trouvé : {data_file}")
        print("💡 Exécutez d'abord : python -m github_profile.core.updater")
        return 1

    print("🌙 Génération des sections README...")
    print(f"📁 Données : {data_file}")

    data = load_projects_data(data_file)
    generate_readme_sections(data, output_file)

    print(f"\n✅ Terminé ! Ouvrez {output_file} pour voir les sections générées.")
    print("💡 Vous pouvez copier-coller ces sections dans votre README.md")

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
