#!/usr/bin/env python3
"""
Génère metrics_for_badges.json pour créer des badges dynamiques
à partir de aggregated_metrics.json
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Any, Optional


def format_number(num: int) -> str:
    """Formate un nombre avec séparateurs de milliers."""
    return f"{num:,}".replace(",", " ")


def create_badges_metrics() -> None:
    """Crée metrics_for_badges.json."""
    # Chemins
    repo_root = Path(__file__).parent.parent
    # Chercher dans le même répertoire (pour GitHub Actions) ou dans le parent (pour local)
    metrics_paths = [
        repo_root / "arkalia-metrics-collector" / "metrics" / "aggregated_metrics.json",
        repo_root / ".." / "arkalia-metrics-collector" / "metrics" / "aggregated_metrics.json",
    ]
    metrics_path: Optional[Path] = None
    for path in metrics_paths:
        if path.exists():
            metrics_path = path
            break

    if metrics_path is None:
        metrics_path = metrics_paths[0]  # Utiliser le premier pour les messages d'erreur

    # Déterminer le chemin de sortie en fonction du chemin trouvé
    if metrics_path and metrics_path.exists():
        output_path = metrics_path.parent / "metrics_for_badges.json"
    else:
        # Fallback vers le premier chemin
        output_path = (
            repo_root / "arkalia-metrics-collector" / "metrics" / "metrics_for_badges.json"
        )

    # Vérifier que le fichier metrics existe
    if not metrics_path.exists():
        print(f"⚠️  Fichier metrics non trouvé: {metrics_path}")
        print("   Utilisation des métriques par défaut")
        default_metrics = {
            "total_modules": 52320,
            "total_tests": 11204,
            "total_lines_of_code": 24790076,
            "total_documentation_files": 6530,
        }
    else:
        # Lire aggregated_metrics.json
        try:
            with open(metrics_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ Erreur lecture metrics: {e}")
            return

        agg = data.get("aggregated", {})
        default_metrics = {
            "total_modules": agg.get("total_modules", 52320),
            "total_tests": agg.get("total_tests", 11204),
            "total_lines_of_code": agg.get("total_lines_of_code", 24790076),
            "total_documentation_files": agg.get("total_documentation_files", 6530),
        }

    # Créer structure pour badges
    badges_metrics: dict[str, dict[str, Any]] = {
        "modules": {
            "value": default_metrics["total_modules"],
            "formatted": format_number(default_metrics["total_modules"]),
            "badge_url": (
                f"https://img.shields.io/badge/Python%20Modules-"
                f"{format_number(default_metrics['total_modules'])}-blue"
            ),
        },
        "tests": {
            "value": default_metrics["total_tests"],
            "formatted": format_number(default_metrics["total_tests"]),
            "badge_url": (
                f"https://img.shields.io/badge/Tests-"
                f"{format_number(default_metrics['total_tests'])}-green"
            ),
        },
        "lines_of_code": {
            "value": default_metrics["total_lines_of_code"],
            "formatted": format_number(default_metrics["total_lines_of_code"]),
            "badge_url": (
                f"https://img.shields.io/badge/Lines%20of%20Code-"
                f"{format_number(default_metrics['total_lines_of_code'])}-orange"
            ),
        },
        "documentation": {
            "value": default_metrics["total_documentation_files"],
            "formatted": format_number(default_metrics["total_documentation_files"]),
            "badge_url": (
                f"https://img.shields.io/badge/Documentation-"
                f"{format_number(default_metrics['total_documentation_files'])}%20files-purple"
            ),
        },
    }

    badges_data: dict[str, Any] = {
        "updated_at": datetime.now().isoformat(),
        "metrics": badges_metrics,
    }

    # Écrire metrics_for_badges.json
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(badges_data, f, indent=2, ensure_ascii=False)
        print(f"✅ {output_path.name} créé avec succès")
    except Exception as e:
        print(f"❌ Erreur écriture badges: {e}")
        return

    # Afficher résumé
    print("\n📊 Badges générés:")
    for key, value in badges_metrics.items():
        print(f"   - {key}: {value['formatted']}")


if __name__ == "__main__":
    create_badges_metrics()
