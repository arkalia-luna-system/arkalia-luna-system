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
from typing import Any


def load_projects_data(data_file: Path) -> dict[str, Any]:
    """Charge les données des projets"""
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)
            return data
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {data_file}")
        return {}


def check_projects_count(data: dict[str, Any], readme_path: Path) -> list[str]:
    """Vérifie que le nombre de projets est cohérent"""
    issues: list[str] = []

    projects = data.get("projects", [])
    total_projects = len(projects)
    stats_total = data.get("stats", {}).get("total_projects", 0)

    if total_projects != stats_total:
        issues.append(
            f"⚠️  Incohérence : {total_projects} projets dans la liste mais {stats_total} dans les stats"
        )

    return issues


def check_projects_list(data: dict[str, Any], readme_path: Path) -> list[str]:
    """Vérifie que tous les projets sont dans le README"""
    issues: list[str] = []

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


def check_workflows(workflows_dir: Path) -> list[str]:
    """Vérifie que les workflows existent"""
    issues: list[str] = []

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


def check_scripts(scripts_dir: Path) -> list[str]:
    """Vérifie que les scripts existent"""
    issues: list[str] = []

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

    all_issues: list[str] = []

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
