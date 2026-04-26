#!/usr/bin/env python3
"""
🔍 Script de Vérification de Cohérence
Vérifie que tous les fichiers sont cohérents entre eux

Usage:
    python scripts/verify-consistency.py
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def load_projects_data(data_file: Path) -> Dict[str, Any]:
    """Charge les données des projets"""
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)
            return data
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {data_file}")
        return {}


def check_projects_count(data: Dict[str, Any], readme_path: Path) -> List[str]:
    """Vérifie que le nombre de projets est cohérent"""
    issues: List[str] = []

    projects = data.get("projects", [])
    total_projects = len(projects)
    stats_total = data.get("stats", {}).get("total_projects", 0)

    if total_projects != stats_total:
        issues.append(
            f"⚠️  Incohérence : {total_projects} projets dans la liste mais {stats_total} dans les stats"
        )

    # Vérifie dans le README
    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8", errors="ignore")
        # Cherche "12 projets" ou similaire
        if (
            f"{total_projects} projets" not in content
            and f"{total_projects} en production" not in content
        ):
            # Vérifie si c'est mentionné différemment
            if "11 projets" in content and total_projects == 12:
                issues.append("⚠️  README mentionne 11 projets mais il y en a 12")
            elif "12 projets" not in content and "12 en production" not in content:
                issues.append(f"💡 README devrait mentionner {total_projects} projets")

    return issues


def check_projects_list(data: Dict[str, Any], readme_path: Path) -> List[str]:
    """Vérifie que tous les projets sont dans le README"""
    issues: List[str] = []

    projects = data.get("projects", [])

    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8", errors="ignore")

        for project in projects:
            name = project.get("name", "")
            github_url = project.get("github_url", "")

            # Vérifie que le projet est mentionné dans le README
            if name not in content and github_url not in content:
                issues.append(f"⚠️  Projet '{name}' non trouvé dans README")

    return issues


def check_workflows(workflows_dir: Path) -> List[str]:
    """Vérifie que les workflows existent"""
    issues: List[str] = []

    expected_workflows = [
        "update-profile.yml",
        "update-metrics.yml",
        "update-complete.yml",
        "ci.yml",
    ]

    for workflow in expected_workflows:
        workflow_path = workflows_dir / workflow
        if not workflow_path.exists():
            issues.append(f"⚠️  Workflow manquant : {workflow}")

    return issues


def check_scripts(scripts_dir: Path) -> List[str]:
    """Vérifie que les scripts existent"""
    issues: List[str] = []

    expected_scripts = [
        "update_readme_metrics.py",
        "create_badges_metrics.py",
        "audit-projects.py",
        "update-all.sh",
    ]

    for script in expected_scripts:
        script_path = scripts_dir / script
        if not script_path.exists():
            issues.append(f"⚠️  Script manquant : {script}")

    return issues


def main() -> int:
    script_dir = Path(__file__).parent.parent
    data_file = script_dir / "config" / "projects-data.json"
    readme_path = script_dir / "README.md"
    workflows_dir = script_dir / ".github" / "workflows"
    scripts_dir = script_dir / "scripts"

    print("🔍 Vérification de cohérence...")
    print("=" * 60)

    # Charge les données
    data = load_projects_data(data_file)
    if not data:
        print("❌ Impossible de charger les données")
        return 1

    all_issues: List[str] = []

    # Vérifications
    print("\n📊 Vérification du nombre de projets...")
    issues = check_projects_count(data, readme_path)
    all_issues.extend(issues)
    if issues:
        for issue in issues:
            print(f"  {issue}")
    else:
        print("  ✅ Nombre de projets cohérent")

    print("\n📋 Vérification de la liste des projets...")
    issues = check_projects_list(data, readme_path)
    all_issues.extend(issues)
    if issues:
        for issue in issues:
            print(f"  {issue}")
    else:
        print("  ✅ Tous les projets sont dans le README")

    print("\n🔄 Vérification des workflows...")
    issues = check_workflows(workflows_dir)
    all_issues.extend(issues)
    if issues:
        for issue in issues:
            print(f"  {issue}")
    else:
        print("  ✅ Tous les workflows sont présents")

    print("\n📜 Vérification des scripts...")
    issues = check_scripts(scripts_dir)
    all_issues.extend(issues)
    if issues:
        for issue in issues:
            print(f"  {issue}")
    else:
        print("  ✅ Tous les scripts sont présents")

    # Résumé
    print("\n" + "=" * 60)
    if all_issues:
        print(f"⚠️  {len(all_issues)} problème(s) trouvé(s)")
        return 1
    else:
        print("✅ Tous les fichiers sont cohérents !")
        return 0


if __name__ == "__main__":
    sys.exit(main())
