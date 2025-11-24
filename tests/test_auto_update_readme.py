#!/usr/bin/env python3
"""
Tests basiques pour auto-update-readme.py
"""

import sys
from pathlib import Path

# Ajoute le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import dynamique pour gérer le nom avec tirets
import importlib.util

spec = importlib.util.spec_from_file_location(
    "auto_update_readme", Path(__file__).parent.parent / "auto-update-readme.py"
)
if spec is None or spec.loader is None:
    raise ImportError("Impossible de charger le module auto-update-readme.py")
auto_update_readme = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auto_update_readme)

generate_stats_section_markdown = auto_update_readme.generate_stats_section_markdown
generate_projects_table = auto_update_readme.generate_projects_table
generate_vision_section = auto_update_readme.generate_vision_section
generate_featured_projects = auto_update_readme.generate_featured_projects


def test_generate_stats_section():
    """Test de génération de la section stats"""
    stats = {
        "total_projects": 12,
        "languages": {"Python": 10, "Dart": 1},
    }
    result = generate_stats_section_markdown(stats)
    assert "12" in result
    assert "Python" in result
    print("✅ test_generate_stats_section: OK")


def test_generate_projects_table():
    """Test de génération du tableau des projets"""
    projects = [
        {
            "name": "test-project",
            "github_url": "https://github.com/test/test-project",
            "description": "Test project description",
            "language": "Python",
        }
    ]
    result = generate_projects_table(projects)
    assert "test-project" in result
    assert "Python" in result
    print("✅ test_generate_projects_table: OK")


def test_generate_vision_section():
    """Test de génération de la section vision"""
    projects = [
        {
            "name": "test-prod",
            "description": "Production project",
        },
        {
            "name": "test-template",
            "description": "Template project",
        },
    ]
    result = generate_vision_section(projects)
    assert "Architecture" in result
    assert "test-prod" in result or "Production" in result
    print("✅ test_generate_vision_section: OK")


def test_generate_featured_projects():
    """Test de génération des featured projects"""
    projects = [
        {
            "name": "test-pro",
            "description": "Production-ready project with tests",
            "stars": 10,
        }
    ]
    result = generate_featured_projects(projects)
    # Peut être vide si score trop bas, mais ne doit pas crasher
    assert isinstance(result, str)
    print("✅ test_generate_featured_projects: OK")


def main():
    """Exécute tous les tests"""
    print("🧪 Tests pour auto-update-readme.py\n")
    try:
        test_generate_stats_section()
        test_generate_projects_table()
        test_generate_vision_section()
        test_generate_featured_projects()
        print("\n✅ Tous les tests passent !")
        return 0
    except AssertionError as e:
        print(f"\n❌ Test échoué : {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
