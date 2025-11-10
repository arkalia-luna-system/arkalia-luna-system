#!/usr/bin/env python3
"""
🌙 Mise à Jour Automatique du README Principal
Met à jour les sections marquées dans README.md avec les données générées

Usage:
    python auto-update-readme.py [--dry-run]
"""

import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple


def load_projects_data(data_file: Path) -> Dict[str, Any]:
    """Charge les données des projets"""
    with open(data_file, "r", encoding="utf-8") as f:
        data: Dict[str, Any] = json.load(f)
        return data


def generate_stats_section_markdown(stats: Dict[str, Any]) -> str:
    """Génère la section statistiques en markdown"""
    # Compte les langages avec formatage
    lang_list = []
    if stats.get("languages"):
        for lang, count in sorted(stats["languages"].items(), key=lambda x: x[1], reverse=True):
            lang_list.append(f"{lang} ({count})")
        lang_str = ", ".join(lang_list)
    else:
        lang_str = "N/A"

    lines = [
        "### 📈 Statistiques",
        "",
        f"- **Projets** : {stats['total_projects']} en production",
        f"- **Langages** : {lang_str}",
        "",
        "<sub>*Dernière mise à jour : novembre 2025*</sub>",
    ]

    return "\n".join(lines)


def generate_languages_table(stats: Dict[str, Any]) -> str:
    """Génère le tableau des langages (non utilisé actuellement, format intégré dans stats)"""
    # Cette fonction n'est plus utilisée car les langages sont dans la section stats
    return ""


def generate_projects_table(projects: List[Dict[str, Any]]) -> str:
    """Génère le tableau des projets depuis les données JSON"""
    lines = [
        "| Projet | Description | Stack | Status |",
        "|:------:|:-----------:|:-----:|:-----:|",
    ]

    for project in projects:
        name = project.get("name", "")
        github_url = project.get("github_url", "")
        description = project.get("description", "") or "Projet en développement"
        language = project.get("language", "Python")

        # Détermine le statut basé sur le nom ou la description
        status = "✅ Production"
        name_lower = name.lower()
        if "template" in name_lower or "base" in name_lower:
            status = "✅ Template"
        elif "beta" in name_lower or "cia" in name_lower:
            status = "🚧 Beta"
        elif "enterprise" in name_lower or "pro" in name_lower or "athalia" in name_lower:
            status = "🚀 Enterprise"

        # Stack intelligent basé sur description et nom
        desc_lower = description.lower()
        name_lower = name.lower()
        stack = language

        # Détection intelligente du stack
        if "flutter" in desc_lower or "flutter" in name_lower:
            stack = "Flutter"
        elif "fastapi" in desc_lower or "fastapi" in name_lower:
            if "docker" in desc_lower:
                stack = "FastAPI + Docker"
            else:
                stack = "FastAPI"
        elif "flask" in desc_lower or "flask" in name_lower:
            stack = "Flask + IA"
        elif "docker" in desc_lower or "container" in desc_lower or "docker" in name_lower:
            stack = f"{language} + Docker"
        elif "mujoco" in desc_lower or "mujoco" in name_lower:
            stack = f"{language} + MuJoCo"
        elif "pytorch" in desc_lower:
            stack = f"{language} + PyTorch"
        elif "design" in desc_lower or "branding" in name_lower:
            stack = "Design"
        elif "template" in name_lower or "base" in name_lower:
            stack = "FastAPI"  # Templates sont généralement FastAPI
        elif "devops" in desc_lower or "pipeline" in name_lower:
            stack = "FastAPI"  # DevOps tools
        elif "metrics" in name_lower or "collector" in name_lower:
            stack = f"{language} + CLI"

        # Limite la description
        desc_short = description[:80] + "..." if len(description) > 80 else description

        lines.append(f"| **[{name}]({github_url})** | {desc_short} | {stack} | {status} |")

    return "\n".join(lines)


def find_section_markers(content: str) -> List[Tuple[int, int, str]]:
    """Trouve les marqueurs de sections dans le README"""
    markers = []

    # Pattern pour <!-- AUTO-UPDATE:section-name -->
    pattern = r"<!--\s*AUTO-UPDATE:(\w+)\s*-->"

    for match in re.finditer(pattern, content):
        start = match.start()
        section_name = match.group(1)

        # Trouve la fin de la section (prochaine section ou marqueur)
        end_pattern = r"(?:<!--\s*AUTO-UPDATE:\w+\s*-->|^##\s+)"
        end_match = re.search(end_pattern, content[start + 1 :], re.MULTILINE)

        if end_match:
            end = start + 1 + end_match.start()
        else:
            end = len(content)

        markers.append((start, end, section_name))

    return markers


def update_readme_section(
    content: str, section_name: str, new_content: str, dry_run: bool = False
) -> Tuple[str, bool]:
    """Met à jour une section du README"""

    # Trouve le marqueur
    pattern = rf"<!--\s*AUTO-UPDATE:{section_name}\s*-->"
    match = re.search(pattern, content)

    if not match:
        print(f"⚠️  Marqueur <!-- AUTO-UPDATE:{section_name} --> non trouvé")
        return content, False

    start = match.end()

    # Trouve la fin de la section
    # Cherche jusqu'à la prochaine section (##) ou le prochain marqueur
    end_pattern = r"(?:<!--\s*AUTO-UPDATE:\w+\s*-->|^##\s+|^---\s*$)"
    end_match = re.search(end_pattern, content[start:], re.MULTILINE)

    if end_match:
        end = start + end_match.start()
    else:
        end = len(content)

    # Remplace le contenu
    before = content[:start]
    after = content[end:]

    new_section = f"\n{new_content}\n"

    if dry_run:
        print(f"\n📝 Section '{section_name}' serait mise à jour :")
        print("=" * 60)
        print(new_section)
        print("=" * 60)
        return content, True

    updated_content = before + new_section + after

    return updated_content, True


def add_section_markers_to_readme(readme_path: Path) -> bool:
    """Ajoute les marqueurs de sections si absents"""
    content = readme_path.read_text(encoding="utf-8")

    markers_added = False

    # Marqueur pour statistiques
    if "<!-- AUTO-UPDATE:stats -->" not in content:
        # Cherche la section statistiques
        stats_pattern = r"(###\s+\*\*📈\s+Statistiques\s+Globales\*\*)"
        match = re.search(stats_pattern, content, re.IGNORECASE)

        if match:
            insert_pos = match.start()
            marker = "<!-- AUTO-UPDATE:stats -->\n\n"
            content = content[:insert_pos] + marker + content[insert_pos:]
            markers_added = True
            print("✅ Marqueur stats ajouté")

    # Marqueur pour langages
    if "<!-- AUTO-UPDATE:languages -->" not in content:
        # Cherche après les statistiques
        lang_pattern = r"(###\s+\*\*💻\s+.*Langage)"
        match = re.search(lang_pattern, content, re.IGNORECASE)

        if not match:
            # Ajoute après les stats si section langages n'existe pas
            stats_end = content.find("### **📈 Statistiques Globales**")
            if stats_end != -1:
                # Trouve la fin de la section stats
                next_section = re.search(r"^##\s+", content[stats_end:], re.MULTILINE)
                if next_section:
                    insert_pos = stats_end + next_section.start()
                    marker = "\n\n<!-- AUTO-UPDATE:languages -->\n\n"
                    content = content[:insert_pos] + marker + content[insert_pos:]
                    markers_added = True
                    print("✅ Marqueur languages ajouté")

    if markers_added:
        readme_path.write_text(content, encoding="utf-8")
        print("✅ Marqueurs ajoutés au README")

    return markers_added


def main():
    parser = argparse.ArgumentParser(description="🌙 Mise à jour automatique du README principal")
    parser.add_argument("--dry-run", action="store_true", help="Mode test (ne modifie rien)")
    parser.add_argument(
        "--add-markers", action="store_true", help="Ajoute les marqueurs de sections si absents"
    )
    parser.add_argument(
        "--readme",
        type=str,
        default="README.md",
        help="Fichier README à mettre à jour (défaut: README.md)",
    )

    args = parser.parse_args()

    script_dir = Path(__file__).parent
    data_file = script_dir / "config" / "projects-data.json"
    readme_path = script_dir / args.readme

    if not data_file.exists():
        print(f"❌ Fichier non trouvé : {data_file}")
        print("💡 Exécutez d'abord : ./scripts/update-all.sh")
        return 1

    if not readme_path.exists():
        print(f"❌ README non trouvé : {readme_path}")
        return 1

    print("🌙 Mise à jour automatique du README...")
    print(f"📁 Données : {data_file}")
    print(f"📄 README : {readme_path}")

    if args.dry_run:
        print("\n🔍 Mode DRY-RUN (aucune modification)")

    # Charge les données
    data = load_projects_data(data_file)
    stats = data.get("stats", {})
    projects = data.get("projects", [])

    # Lit le README
    content = readme_path.read_text(encoding="utf-8")

    # Ajoute les marqueurs si demandé
    if args.add_markers:
        add_section_markers_to_readme(readme_path)
        content = readme_path.read_text(encoding="utf-8")

    updated = False

    # Met à jour la section stats
    stats_content = generate_stats_section_markdown(stats)
    content, stats_updated = update_readme_section(content, "stats", stats_content, args.dry_run)
    if stats_updated:
        updated = True
        print("✅ Section stats mise à jour")

    # Met à jour la section langages
    lang_content = generate_languages_table(stats)
    if lang_content:
        content, lang_updated = update_readme_section(
            content, "languages", lang_content, args.dry_run
        )
        if lang_updated:
            updated = True
            print("✅ Section languages mise à jour")

    # Met à jour le tableau des projets si marqueur présent
    if "<!-- AUTO-UPDATE:projects -->" in content:
        projects_content = generate_projects_table(projects)
        content, projects_updated = update_readme_section(
            content, "projects", projects_content, args.dry_run
        )
        if projects_updated:
            updated = True
            print("✅ Tableau des projets mis à jour")

    # Sauvegarde si pas en dry-run
    if updated and not args.dry_run:
        readme_path.write_text(content, encoding="utf-8")
        print(f"\n✅ README mis à jour : {readme_path}")
    elif args.dry_run:
        print("\n🔍 Mode DRY-RUN : Aucune modification effectuée")
    else:
        print("\n⚠️  Aucune section mise à jour")
        print("💡 Ajoutez des marqueurs <!-- AUTO-UPDATE:stats --> dans votre README")
        print("   Ou utilisez --add-markers pour les ajouter automatiquement")

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
