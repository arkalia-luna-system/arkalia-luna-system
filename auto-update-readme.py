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
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime, timezone


def _clean_description(raw_description: Optional[str], max_length: int = 100) -> str:
    """Nettoie une description brute pour affichage markdown lisible."""
    if not raw_description:
        return "Projet en développement"

    desc = raw_description.strip()

    # Supprime syntaxe markdown fréquente introduite par extraction README.
    desc = re.sub(r"^[>\-\*\s]+", "", desc)
    desc = desc.replace("**", "").replace("__", "")
    desc = re.sub(r"`([^`]*)`", r"\1", desc)
    desc = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", desc)
    desc = re.sub(r"\s+", " ", desc).strip()

    # Retire les symboles/emoji en tête pour éviter artefacts visuels.
    desc = re.sub(r"^[^0-9A-Za-zÀ-ÿ]+", "", desc).strip()

    if not desc:
        return "Projet en développement"

    if len(desc) > max_length:
        return desc[: max_length - 3].rstrip() + "..."
    return desc


def load_projects_data(data_file: Path) -> Dict[str, Any]:
    """Charge les données des projets"""
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier de données non trouvé : {data_file}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Erreur de décodage JSON dans {data_file}: {e}")


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
        f"- **Projets** : {stats.get('total_projects', 0)} au total",
        f"- **Langages** : {lang_str}",
        "",
        f"<sub>*Dernière mise à jour : {datetime.now().strftime('%d %B %Y')}*</sub>".replace(
            "January", "janvier"
        )
        .replace("February", "février")
        .replace("March", "mars")
        .replace("April", "avril")
        .replace("May", "mai")
        .replace("June", "juin")
        .replace("July", "juillet")
        .replace("August", "août")
        .replace("September", "septembre")
        .replace("October", "octobre")
        .replace("November", "novembre")
        .replace("December", "décembre"),
    ]

    return "\n".join(lines)


def generate_languages_table(stats: Dict[str, Any]) -> str:
    """Génère le tableau des langages (non utilisé actuellement, format intégré dans stats)"""
    # Cette fonction n'est plus utilisée car les langages sont dans la section stats
    return ""


def generate_vision_section(projects: List[Dict[str, Any]]) -> str:
    """Génère automatiquement la section Vision Système depuis projects-data.json"""
    # Groupe les projets par rôle
    prod_projects: List[Dict[str, Any]] = []
    design_projects: List[Dict[str, Any]] = []
    tooling_projects: List[Dict[str, Any]] = []
    archive_projects: List[Dict[str, Any]] = []

    for project in projects:
        name = (project.get("name") or "").lower()
        desc = (project.get("description") or "").lower()

        # Classification
        if "template" in name or "base" in name:
            tooling_projects.append(project)
        elif "metrics" in name or "collector" in name:
            tooling_projects.append(project)
        elif "pipeline" in name or "devops" in desc or "athalia" in name:
            tooling_projects.append(project)
        elif "archive" in name or "nours" in name or "poc" in desc:
            archive_projects.append(project)
        elif "branding" in name or "logo" in name:
            design_projects.append(project)
        elif "luna-system" in name or "profile" in desc or "profil" in desc:
            tooling_projects.append(project)
        else:
            prod_projects.append(project)

    lines = [
        "### 🏗️ Architecture de l'Écosystème",
        "",
        "L'écosystème est organisé en **4 catégories principales** :",
        "",
    ]

    # Projets Production
    if prod_projects:
        lines.append("#### 🏢 **Projets Produits**")
        lines.append("Projets actifs, suivis et maintenus :")
        for proj in prod_projects[:6]:  # Limite à 6 pour lisibilité
            name = proj.get("name", "")
            desc = _clean_description(proj.get("description"), max_length=63)
            lines.append(f"- **{name}** : {desc}")
        lines.append("")

    # Design & Branding
    if design_projects:
        lines.append("#### 🎨 **Design & Branding**")
        lines.append("Outils de génération et identité visuelle :")
        for proj in design_projects:
            name = proj.get("name", "")
            desc = _clean_description(proj.get("description"), max_length=63)
            lines.append(f"- **{name}** : {desc}")
        lines.append("")

    # Outils & Infrastructure
    if tooling_projects:
        lines.append("#### 🔧 **Outils & Infrastructure**")
        lines.append("Infrastructure et outils de développement :")
        for proj in tooling_projects[:5]:  # Limite à 5
            name = proj.get("name", "")
            desc = _clean_description(proj.get("description"), max_length=63)
            lines.append(f"- **{name}** : {desc}")
        lines.append("")

    # Archives
    if archive_projects:
        lines.append("#### 📦 **Archives**")
        lines.append("Projets historiques conservés pour leur valeur pédagogique :")
        for proj in archive_projects:
            name = proj.get("name", "")
            desc = _clean_description(proj.get("description"), max_length=63)
            lines.append(f"- **{name}** : {desc}")
        lines.append("")

    return "\n".join(lines)


def _format_relative_time(iso_timestamp: Optional[str]) -> str:
    """Formate un timestamp ISO GitHub (pushed_at) en temps relatif lisible."""
    if not iso_timestamp:
        return "N/A"

    try:
        # GitHub renvoie du ISO8601 avec 'Z' (UTC)
        ts = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
    except ValueError:
        return iso_timestamp

    now = datetime.now(timezone.utc)
    delta = now - ts

    seconds = int(delta.total_seconds())
    if seconds < 60:
        return "il y a quelques secondes"
    minutes = seconds // 60
    if minutes < 60:
        return f"il y a {minutes} min"
    hours = minutes // 60
    if hours < 48:
        return f"il y a {hours} h"
    days = hours // 24
    if days < 60:
        return f"il y a {days} j"

    months = days // 30
    if months < 24:
        return f"il y a {months} mois"

    years = months // 12
    return f"il y a {years} an(s)"


def generate_status_board(projects: List[Dict[str, Any]]) -> str:
    """Génère un tableau de bord cyberpunk des systèmes clés."""
    if not projects:
        return ""

    # Ordre d'affichage prioritaire
    priority_order = [
        "arkalia-luna-pro",
        "arkalia-cia",
        "Arkalia-aria",
        "Arkalia-luna-logo",
        "bbia-sim",
        "arkalia-quest",
        "arkalia-metrics-collector",
        "arkalia-luna-system",
    ]

    indexed: Dict[str, Dict[str, Any]] = {p.get("name", ""): p for p in projects}

    def _classify(project: Dict[str, Any]) -> Tuple[str, str]:
        """Retourne (role, status) avec une classification prudente."""
        name = (project.get("name") or "").lower()
        desc = (project.get("description") or "").lower()

        role = "Core"
        status = "ACTIF"

        if "luna-system" in name or "profile" in desc or "profil" in desc:
            role = "Profil"
        elif "template" in name or "base" in name:
            role = "Tooling"
        elif "metrics" in name or "collector" in name:
            role = "Metrics"
        elif "pipeline" in name or "devops" in desc or "athalia" in name:
            role = "DevOps"
        elif "branding" in name or "logo" in name:
            role = "Design"
        elif "cia" in name or "aria" in name:
            role = "Santé / Mobile"
        elif "quest" in name:
            role = "Gaming"
        elif "bbia" in name or "robot" in desc:
            role = "Robotique"

        if "beta" in name or "beta" in desc or "cia" in name:
            status = "BETA"
        elif "archive" in name or "nours" in name or "poc" in desc:
            status = "ARCHIVE"

        return role, status

    rows: List[Tuple[int, Dict[str, Any]]] = []
    for idx, name in enumerate(priority_order):
        proj = indexed.get(name)
        if not proj:
            continue
        rows.append((idx, proj))

    if not rows:
        return ""

    # Construire le markdown
    lines: List[str] = [
        "### 🔮 Tableau de Bord Système",
        "",
        "_Vue temps réel des modules principaux de l'écosystème Arkalia Luna System._",
        "",
        "| Module | Rôle | Statut | Dernier commit | Branche par défaut |",
        "|:------:|:----:|:------:|:--------------:|:-------------------:|",
    ]

    for _, proj in rows:
        name = proj.get("name", "")
        github_url = proj.get("github_url", "")
        default_branch = proj.get("default_branch", "main")
        pushed_at = proj.get("pushed_at")

        role, status = _classify(proj)

        status_label = {
            "ACTIF": "🟢 ACTIF",
            "BETA": "🟡 BETA",
            "ARCHIVE": "⚫ ARCHIVE",
        }.get(status, status)

        last_commit = _format_relative_time(pushed_at)

        module_label = f"**[{name}]({github_url})**" if github_url else f"**{name}**"

        lines.append(
            f"| {module_label} | {role} | `{status_label}` | {last_commit} | `{default_branch}` |"
        )

    return "\n".join(lines)


def generate_featured_projects(projects: List[Dict[str, Any]]) -> str:
    """Génère automatiquement les Featured Projects avec scoring"""
    # Score chaque projet
    scored_projects = []

    for project in projects:
        name = (project.get("name") or "").lower()
        desc = (project.get("description") or "").lower()
        stars = project.get("stars", 0)

        score = 0

        # Critères de scoring
        if "pro" in name or "enterprise" in desc:
            score += 30
        if "production-ready" in desc or "production" in desc:
            score += 20
        if "test" in desc and any(char.isdigit() for char in desc):
            score += 15
        if "coverage" in desc or "couverture" in desc:
            score += 10
        if stars > 0:
            score += stars * 2
        if "docker" in desc or "monitoring" in desc:
            score += 10
        if "ia" in desc or "ai" in desc or "robot" in desc:
            score += 5

        # Exclut certains projets
        if "template" in name or "archive" in name or "nours" in name:
            score = 0

        scored_projects.append((score, project))

    # Trie par score et prend les top 3
    scored_projects.sort(key=lambda x: x[0], reverse=True)
    top_projects = [p[1] for p in scored_projects[:3] if p[0] > 0]

    if not top_projects:
        return ""

    lines = [
        "**Trois systèmes représentatifs de l’écosystème (architecture, usage, outillage).**",
        "",
    ]

    # Génère le tableau HTML (format existant)
    lines.append('<div align="center">')
    lines.append("")
    lines.append("<table>")
    lines.append("<tr>")

    for i, project in enumerate(top_projects):
        name = project.get("name", "")
        github_url = project.get("github_url", "")
        desc = _clean_description(project.get("description"), max_length=53)

        # Image par défaut (logo Arkalia)
        img_url = "https://raw.githubusercontent.com/arkalia-luna-system/arkalia-luna-logo/main/exports/screenshots/ultimate-serenity-200.svg"

        lines.append('<td align="center" width="33%">')
        lines.append(f'<a href="{github_url}">')
        lines.append(
            f'<img src="{img_url}" width="120" height="120" style="border-radius: 20px; box-shadow: 0 10px 20px rgba(20, 184, 166, 0.4);" alt="{name}"/>'
        )
        lines.append("<br/><br/>")
        lines.append(f"<strong>{name}</strong>")
        lines.append("<br/>")
        lines.append(f"<sub>{desc}</sub>")
        lines.append("</a>")
        lines.append("</td>")

    lines.append("</tr>")
    lines.append("</table>")
    lines.append("")
    lines.append("</div>")

    return "\n".join(lines)


def generate_projects_table(projects: List[Dict[str, Any]]) -> str:
    """Génère le tableau des projets depuis les données JSON"""
    lines = [
        "| Projet | Description | Stack | Rôle | Status |",
        "|:------:|:-----------:|:-----:|:----:|:-----:|",
    ]

    for project in projects:
        name = project.get("name", "")
        github_url = project.get("github_url", "")
        description = _clean_description(project.get("description"), max_length=100)
        language = project.get("language", "Python")

        # Détermine le statut de manière conservative (sans sur-promesse)
        status = "🟢 Actif"
        name_lower = name.lower()
        if "template" in name_lower or "base" in name_lower:
            status = "🧩 Template"
        elif "beta" in name_lower or "cia" in name_lower:
            status = "🚧 Beta"
        elif "archive" in name_lower or "nours" in name_lower:
            status = "📦 Archivé"

        # Détermine le rôle basé sur le nom et la description
        role = "🏢 Projet"
        desc_lower = description.lower()
        if "luna-system" in name_lower or "profile" in desc_lower or "profil" in desc_lower:
            role = "🌙 Profil"  # Profil GitHub centralisé
        elif "template" in name_lower or "base" in name_lower:
            role = "🔧 Tooling"
        elif "metrics" in name_lower or "collector" in name_lower:
            role = "🔧 Tooling"
        elif "pipeline" in name_lower or "devops" in desc_lower or "athalia" in name_lower:
            role = "🔧 Tooling"
        elif "archive" in name_lower or "nours" in name_lower or "poc" in desc_lower:
            role = "📦 Archive"
        elif "beta" in name_lower or "cia" in name_lower:
            role = "🚧 Beta"

        # Stack intelligent basé sur description et nom
        stack = language

        # Détection intelligente du stack (améliorée)
        stack_parts = []

        # Framework principal
        if "flutter" in desc_lower or "flutter" in name_lower or "dart" in language.lower():
            stack_parts.append("Flutter")
        elif "fastapi" in desc_lower or "fastapi" in name_lower:
            stack_parts.append("FastAPI")
        elif "flask" in desc_lower or "flask" in name_lower:
            stack_parts.append("Flask")
        elif language and language != "Python":
            stack_parts.append(language)

        # Technologies additionnelles
        if "docker" in desc_lower or "container" in desc_lower:
            stack_parts.append("Docker")
        if "mujoco" in desc_lower or "mujoco" in name_lower:
            stack_parts.append("MuJoCo")
        if "pytorch" in desc_lower or "torch" in desc_lower:
            stack_parts.append("PyTorch")
        if "prometheus" in desc_lower or "grafana" in desc_lower:
            stack_parts.append("Monitoring")
        if "ia" in desc_lower or "ai" in desc_lower or "intelligence" in desc_lower:
            if "flask" not in stack_parts:
                stack_parts.append("IA")

        # Cas spéciaux
        if "design" in desc_lower or "branding" in name_lower or "logo" in name_lower:
            stack = "Design"
        elif "template" in name_lower or "base" in name_lower:
            stack = "FastAPI"  # Templates sont généralement FastAPI
        elif "metrics" in name_lower or "collector" in name_lower:
            stack = f"{language} + CLI"
        elif "luna-system" in name_lower or "profile" in desc_lower or "profil" in desc_lower:
            stack = "Python"  # Profil GitHub = Python
        elif stack_parts:
            stack = " + ".join(stack_parts)
        else:
            stack = language if language else "Python"

        # Nettoie et limite la description (enlève emojis en début si trop nombreux)
        desc_short = description

        # Échappe les pipes dans la description pour éviter de casser le tableau
        desc_short = desc_short.replace("|", "\\|")

        lines.append(f"| **[{name}]({github_url})** | {desc_short} | {stack} | {role} | {status} |")

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

    # Met à jour la section Vision Système si marqueur présent
    if "<!-- AUTO-UPDATE:vision -->" in content:
        vision_content = generate_vision_section(projects)
        content, vision_updated = update_readme_section(
            content, "vision", vision_content, args.dry_run
        )
        if vision_updated:
            updated = True
            print("✅ Section Vision Système mise à jour")

    # Met à jour le tableau de bord système si marqueur présent
    if "<!-- AUTO-UPDATE:status -->" in content:
        status_content = generate_status_board(projects)
        if status_content:
            content, status_updated = update_readme_section(
                content, "status", status_content, args.dry_run
            )
            if status_updated:
                updated = True
                print("✅ Tableau de bord système mis à jour")

    # Met à jour les Featured Projects si marqueur présent
    if "<!-- AUTO-UPDATE:featured -->" in content:
        featured_content = generate_featured_projects(projects)
        if featured_content:
            content, featured_updated = update_readme_section(
                content, "featured", featured_content, args.dry_run
            )
            if featured_updated:
                updated = True
                print("✅ Featured Projects mis à jour")

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
