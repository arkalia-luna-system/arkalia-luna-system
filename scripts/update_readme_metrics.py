#!/usr/bin/env python3
"""
Met à jour automatiquement les métriques dans README.md
à partir de aggregated_metrics.json
"""

import json
import re
from pathlib import Path
from datetime import datetime


def format_number(num: int) -> str:
    """Formate un nombre avec séparateurs de milliers."""
    return f"{num:,}".replace(",", " ")


def update_readme_metrics():
    """Met à jour les métriques dans README.md."""
    # Chemins
    repo_root = Path(__file__).parent.parent
    metrics_path = (
        repo_root / ".." / "arkalia-metrics-collector" / "metrics" / "aggregated_metrics.json"
    )
    readme_path = repo_root / "README.md"

    # Vérifier que les fichiers existent
    if not metrics_path.exists():
        print(f"⚠️  Fichier metrics non trouvé: {metrics_path}")
        print("   Utilisation des métriques par défaut")
        return

    if not readme_path.exists():
        print(f"❌ README.md non trouvé: {readme_path}")
        return

    # Lire aggregated_metrics.json
    try:
        with open(metrics_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Erreur lecture metrics: {e}")
        return

    agg = data.get("aggregated", {})
    projects = data.get("projects", [])

    # Créer un dictionnaire de coverage par projet
    project_coverage = {}
    for project in projects:
        project_name = project.get("name", "")
        # Le coverage peut être dans les métriques étendues
        # Pour l'instant, on utilise les valeurs hardcodées du README
        # TODO: Intégrer coverage depuis aggregated_metrics.json quand disponible
        project_coverage[project_name] = None

    # Lire README.md
    try:
        readme = readme_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"❌ Erreur lecture README: {e}")
        return

    # Remplacer métriques globales
    total_modules = agg.get('total_modules', 52336)
    total_tests = agg.get('total_tests', 11208)
    total_lines = agg.get('total_lines_of_code', 24792057)
    total_docs = agg.get('total_documentation_files', 6556)
    
    replacements = {
        # Badges et métriques globales (utiliser virgules pour les badges)
        r"52,320_modules": f"{total_modules:,}_modules".replace(",", ","),
        r"11,204_Automated": f"{total_tests:,}_Automated".replace(",", ","),
        r"52 336_modules": f"{total_modules:,}_modules".replace(",", ","),
        r"11 208_Automated": f"{total_tests:,}_Automated".replace(",", ","),
        r"\*\*52,320\*\*": f"**{format_number(total_modules)}**",
        r"\*\*11,204\*\*": f"**{format_number(total_tests)}**",
        r"\*\*24,790,076\*\*": f"**{format_number(total_lines)}**",
        r"52,320 modules": f"{format_number(total_modules)} modules",
        r"11,204 tests": f"{format_number(total_tests)} tests",
        r"24,790,076": format_number(total_lines),
        r"6,530 fichiers": f"{format_number(total_docs)} fichiers",
        r"52,320 Modules": f"{format_number(total_modules)} Modules",
        # Format avec espaces aussi
        r"52 320 modules": f"{format_number(total_modules)} modules",
        r"11 204 tests": f"{format_number(total_tests)} tests",
    }

    for pattern, replacement in replacements.items():
        readme = re.sub(pattern, replacement, readme)
    
    # Mettre à jour les métriques spécifiques par projet
    for project in projects:
        project_name = project.get("name", "")
        project_tests = project.get("tests", 0)
        project_modules = project.get("modules", 0)
        
        # BBIA Reachy Sim
        if ("bbia" in project_name.lower() and "sim" in project_name.lower()) or "reachy" in project_name.lower():
            # Remplacer "1362 tests" ou autres nombres incorrects par le vrai nombre
            readme = re.sub(
                r"\d{1,4}\s+\d{1,4}\s+\d{1,4}\s+tests",
                f"{format_number(project_tests)} tests",
                readme
            )
            readme = re.sub(
                r"1362 tests",
                f"{format_number(project_tests)} tests",
                readme
            )
            # Remplacer aussi les patterns avec espaces multiples
            readme = re.sub(
                r"(\d{1,3}(?:\s+\d{1,3}){2,})\s+tests",
                f"{format_number(project_tests)} tests",
                readme
            )

    # Mettre à jour le coverage global si disponible
    global_coverage = agg.get("global_coverage")
    if global_coverage is not None:
        # Remplacer "~64%" ou autres patterns de coverage global
        readme = re.sub(
            r"~64%|Couverture Tests.*?~64%",
            f"Couverture Tests : {global_coverage:.2f}%",
            readme,
        )
        # Mettre à jour aussi dans le tableau si présent
        readme = re.sub(
            r"Couverture Tests.*?\|\s*~64%",
            f"Couverture Tests | {global_coverage:.2f}%",
            readme,
        )

    # Lire le rapport d'évolution si disponible
    evolution_path = (
        repo_root / ".." / "arkalia-metrics-collector" / "metrics" / "EVOLUTION_REPORT.md"
    )
    if evolution_path.exists():
        try:
            evolution_report = evolution_path.read_text(encoding="utf-8")
            # Extraire les deltas du rapport pour affichage
            delta_pattern = (
                r"\|\s*\*\*Total Modules\*\*\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([^\|]+)\s*\|"
            )
            match = re.search(delta_pattern, evolution_report)
            if match:
                before, after, delta = match.groups()
                if delta.strip() != "N/A":
                    print(f"   - Modules: {before} → {after} ({delta})")
        except Exception as e:
            print(f"⚠️  Erreur lecture rapport évolution: {e}")

    # Mettre à jour la date
    date_pattern = r"\*Métriques collectées automatiquement le \d{4}-\d{2}-\d{2}\*"
    new_date = f"*Métriques collectées automatiquement le {datetime.now().strftime('%Y-%m-%d')}*"
    readme = re.sub(date_pattern, new_date, readme)

    # Écrire README.md
    try:
        readme_path.write_text(readme, encoding="utf-8")
        print("✅ README.md mis à jour avec succès")
    except Exception as e:
        print(f"❌ Erreur écriture README: {e}")
        return

    # Afficher résumé
    print("\n📊 Métriques mises à jour:")
    print(f"   - Modules: {format_number(agg.get('total_modules', 52320))}")
    print(f"   - Tests: {format_number(agg.get('total_tests', 11204))}")
    print(f"   - Lignes: {format_number(agg.get('total_lines_of_code', 24790076))}")
    print(
        f"   - Documentation: {format_number(agg.get('total_documentation_files', 6530))} fichiers"
    )
    global_coverage = agg.get("global_coverage")
    if global_coverage is not None:
        print(f"   - Coverage global: {global_coverage:.2f}%")
    else:
        print("   - Coverage global: N/A (non calculé)")

    # Vérifier si un rapport d'évolution existe
    evolution_path = (
        repo_root / ".." / "arkalia-metrics-collector" / "metrics" / "EVOLUTION_REPORT.md"
    )
    if evolution_path.exists():
        print("   - Rapport d'évolution disponible: EVOLUTION_REPORT.md")


if __name__ == "__main__":
    update_readme_metrics()
