#!/usr/bin/env python3
"""
🔍 Script d'Audit Complet des Projets Arkalia Luna System
Analyse chaque projet : README, structure, métriques, cohérence

Usage:
    python scripts/audit-projects.py [--output OUTPUT_FILE] [--verbose]
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Ajoute le répertoire parent au path pour importer update-profile
sys.path.insert(0, str(Path(__file__).parent.parent))

# Pas besoin d'importer update-profile pour l'audit
# On utilise directement les données JSON


class ProjectAuditor:
    """Auditeur de projets pour analyser la qualité et la cohérence"""

    def __init__(self, projects_data_path: Path):
        self.projects_data_path = projects_data_path
        self.data = self._load_projects_data()
        self.audit_results: List[Dict[str, Any]] = []

    def _load_projects_data(self) -> Dict[str, Any]:
        """Charge les données des projets"""
        try:
            with open(self.projects_data_path, "r", encoding="utf-8") as f:
                data: Dict[str, Any] = json.load(f)
                return data
        except FileNotFoundError:
            print(f"❌ Fichier non trouvé : {self.projects_data_path}")
            print("💡 Exécutez d'abord : python update-profile.py")
            sys.exit(1)

    def audit_readme(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Audite le README d'un projet"""
        readme_path = project.get("readme_path")
        issues: List[str] = []
        strengths: List[str] = []

        if not readme_path:
            issues.append("⚠️  README non trouvé localement")
            return {"has_readme": False, "issues": issues, "strengths": strengths}

        readme_file = Path(readme_path)
        if not readme_file.exists():
            issues.append("⚠️  README indiqué mais fichier introuvable")
            return {"has_readme": False, "issues": issues, "strengths": strengths}

        try:
            content = readme_file.read_text(encoding="utf-8", errors="ignore")
            lines = content.split("\n")

            # Vérifications
            has_title = any(line.startswith("# ") for line in lines[:10])
            has_description = len([line for line in lines[:30] if line.strip() and not line.startswith("#")]) > 0
            has_badges = "[!" in content
            has_installation = "install" in content.lower() or "setup" in content.lower()
            has_usage = "usage" in content.lower() or "example" in content.lower()
            has_tests = "test" in content.lower() or "pytest" in content.lower()
            has_license = "license" in content.lower() or "mit" in content.lower()
            has_contributing = "contribut" in content.lower()

            if has_title:
                strengths.append("✅ Titre clair")
            else:
                issues.append("⚠️  Titre manquant ou peu visible")

            if has_description:
                strengths.append("✅ Description présente")
            else:
                issues.append("⚠️  Description manquante")

            if has_badges:
                strengths.append("✅ Badges présents")
            else:
                issues.append("💡 Badges recommandés (version, tests, coverage)")

            if has_installation:
                strengths.append("✅ Section installation")
            else:
                issues.append("💡 Section installation recommandée")

            if has_usage:
                strengths.append("✅ Exemples d'utilisation")
            else:
                issues.append("💡 Exemples d'utilisation recommandés")

            if has_tests:
                strengths.append("✅ Tests documentés")
            else:
                issues.append("💡 Documentation des tests recommandée")

            if has_license:
                strengths.append("✅ License mentionnée")
            else:
                issues.append("💡 License à clarifier")

            if has_contributing:
                strengths.append("✅ Guide de contribution")
            else:
                issues.append("💡 Guide de contribution recommandé")

            # Longueur du README
            if len(lines) < 50:
                issues.append("💡 README assez court (enrichir avec plus de détails)")
            elif len(lines) > 500:
                strengths.append("✅ Documentation exhaustive")

            return {
                "has_readme": True,
                "lines_count": len(lines),
                "issues": issues,
                "strengths": strengths,
            }

        except Exception as e:
            issues.append(f"❌ Erreur lors de la lecture : {e}")
            return {"has_readme": False, "issues": issues, "strengths": strengths}

    def audit_structure(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Audite la structure d'un projet"""
        local_path = project.get("local_path")
        issues: List[str] = []
        strengths: List[str] = []

        if not local_path:
            issues.append("⚠️  Projet non trouvé localement (impossible d'auditer la structure)")
            return {"found": False, "issues": issues, "strengths": strengths}

        project_path = Path(local_path)
        if not project_path.exists():
            issues.append("⚠️  Chemin indiqué mais dossier introuvable")
            return {"found": False, "issues": issues, "strengths": strengths}

        # Vérifications de structure
        has_tests_dir = (project_path / "tests").exists() or (project_path / "test").exists()
        has_docs_dir = (project_path / "docs").exists() or (project_path / "documentation").exists()
        has_ci = (project_path / ".github").exists() or (project_path / ".gitlab-ci.yml").exists()
        has_docker = (project_path / "Dockerfile").exists() or (project_path / "docker-compose.yml").exists()
        has_requirements = (
            (project_path / "requirements.txt").exists()
            or (project_path / "pyproject.toml").exists()
            or (project_path / "Pipfile").exists()
        )
        has_config = (project_path / "config").exists() or (project_path / ".env.example").exists()

        if has_tests_dir:
            strengths.append("✅ Dossier tests présent")
        else:
            issues.append("💡 Dossier tests recommandé")

        if has_docs_dir:
            strengths.append("✅ Documentation organisée")
        else:
            issues.append("💡 Dossier docs recommandé")

        if has_ci:
            strengths.append("✅ CI/CD configuré")
        else:
            issues.append("💡 CI/CD recommandé")

        if has_docker:
            strengths.append("✅ Docker configuré")
        else:
            issues.append("💡 Docker recommandé pour production")

        if has_requirements:
            strengths.append("✅ Dépendances documentées")
        else:
            issues.append("💡 Fichier requirements recommandé")

        if has_config:
            strengths.append("✅ Configuration organisée")
        else:
            issues.append("💡 Dossier config recommandé")

        return {
            "found": True,
            "has_tests_dir": has_tests_dir,
            "has_docs_dir": has_docs_dir,
            "has_ci": has_ci,
            "has_docker": has_docker,
            "has_requirements": has_requirements,
            "has_config": has_config,
            "issues": issues,
            "strengths": strengths,
        }

    def audit_metrics(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Audite les métriques d'un projet"""
        issues: List[str] = []
        strengths: List[str] = []

        description = project.get("description", "").lower()

        # Détection des métriques dans la description
        has_tests_mention = "test" in description and any(
            word in description for word in ["61", "179", "671", "151", "1362", "tests"]
        )
        has_coverage_mention = "coverage" in description or "couverture" in description
        has_version_mention = "v" in description and any(
            char.isdigit() for char in description.split("v")[-1][:5] if "v" in description
        )

        if has_tests_mention:
            strengths.append("✅ Tests mentionnés dans la description")
        else:
            issues.append("💡 Mentionner le nombre de tests dans la description")

        if has_coverage_mention:
            strengths.append("✅ Coverage mentionné")
        else:
            issues.append("💡 Coverage à mentionner si disponible")

        if has_version_mention:
            strengths.append("✅ Version mentionnée")
        else:
            issues.append("💡 Version à mentionner")

        return {
            "has_tests_mention": has_tests_mention,
            "has_coverage_mention": has_coverage_mention,
            "has_version_mention": has_version_mention,
            "issues": issues,
            "strengths": strengths,
        }

    def audit_coherence(self, project: Dict[str, Any], all_projects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Audite la cohérence avec les autres projets"""
        issues: List[str] = []
        strengths: List[str] = []

        name = project.get("name", "")
        description = project.get("description", "")
        language = project.get("language", "")

        # Vérifie la cohérence du nommage
        if name.startswith("arkalia-") or name.startswith("Arkalia-"):
            strengths.append("✅ Nommage cohérent (préfixe arkalia)")
        elif name.startswith("bbia"):
            strengths.append("✅ Nommage cohérent (préfixe bbia)")
        else:
            issues.append("💡 Considérer un préfixe cohérent (arkalia- ou bbia-)")

        # Vérifie la présence d'une description
        if description and len(description) > 20:
            strengths.append("✅ Description présente et détaillée")
        else:
            issues.append("⚠️  Description manquante ou trop courte")

        # Vérifie la cohérence du langage
        if language:
            strengths.append(f"✅ Langage principal détecté : {language}")
        else:
            issues.append("⚠️  Langage principal non détecté")

        return {
            "issues": issues,
            "strengths": strengths,
        }

    def audit_project(self, project: Dict[str, Any], all_projects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Audite un projet complet"""
        name = project.get("name", "Unknown")
        print(f"\n🔍 Audit de {name}...")

        readme_audit = self.audit_readme(project)
        structure_audit = self.audit_structure(project)
        metrics_audit = self.audit_metrics(project)
        coherence_audit = self.audit_coherence(project, all_projects)

        # Calcul du score global
        total_issues = (
            len(readme_audit.get("issues", []))
            + len(structure_audit.get("issues", []))
            + len(metrics_audit.get("issues", []))
            + len(coherence_audit.get("issues", []))
        )
        total_strengths = (
            len(readme_audit.get("strengths", []))
            + len(structure_audit.get("strengths", []))
            + len(metrics_audit.get("strengths", []))
            + len(coherence_audit.get("strengths", []))
        )

        # Score sur 10 (basé sur forces - issues)
        score = max(0, min(10, 5 + (total_strengths - total_issues) * 0.5))

        return {
            "name": name,
            "github_url": project.get("github_url", ""),
            "readme": readme_audit,
            "structure": structure_audit,
            "metrics": metrics_audit,
            "coherence": coherence_audit,
            "score": round(score, 1),
            "total_issues": total_issues,
            "total_strengths": total_strengths,
        }

    def audit_all(self) -> List[Dict[str, Any]]:
        """Audite tous les projets"""
        projects = self.data.get("projects", [])
        print(f"🔍 Début de l'audit de {len(projects)} projets...\n")

        results = []
        for project in projects:
            audit_result = self.audit_project(project, projects)
            results.append(audit_result)

        return results

    def generate_report(self, results: List[Dict[str, Any]], output_file: Optional[Path] = None) -> str:
        """Génère un rapport d'audit en Markdown"""
        lines = [
            "# 🔍 Rapport d'Audit - Projets Arkalia Luna System",
            "",
            f"**Date** : {datetime.now().strftime('%d %B %Y, %H:%M')}",
            f"**Projets audités** : {len(results)}",
            "",
            "---",
            "",
            "## 📊 Résumé Global",
            "",
        ]

        # Statistiques globales
        total_issues = sum(r.get("total_issues", 0) for r in results)
        total_strengths = sum(r.get("total_strengths", 0) for r in results)
        avg_score = sum(r.get("score", 0) for r in results) / len(results) if results else 0

        lines.extend(
            [
                f"- **Score moyen** : {avg_score:.1f}/10",
                f"- **Points forts totaux** : {total_strengths}",
                f"- **Points à améliorer** : {total_issues}",
                "",
                "---",
                "",
            ]
        )

        # Détails par projet
        lines.append("## 📋 Détails par Projet\n")

        for result in sorted(results, key=lambda x: x.get("score", 0), reverse=True):
            name = result.get("name", "Unknown")
            score = result.get("score", 0)
            github_url = result.get("github_url", "")

            lines.extend(
                [
                    f"### {name}",
                    "",
                    f"**Score** : {score}/10 | [GitHub]({github_url})",
                    "",
                ]
            )

            # Points forts
            strengths = []
            strengths.extend(result.get("readme", {}).get("strengths", []))
            strengths.extend(result.get("structure", {}).get("strengths", []))
            strengths.extend(result.get("metrics", {}).get("strengths", []))
            strengths.extend(result.get("coherence", {}).get("strengths", []))

            if strengths:
                lines.append("**✅ Points forts :**")
                for strength in strengths:
                    lines.append(f"- {strength}")
                lines.append("")

            # Points à améliorer
            issues = []
            issues.extend(result.get("readme", {}).get("issues", []))
            issues.extend(result.get("structure", {}).get("issues", []))
            issues.extend(result.get("metrics", {}).get("issues", []))
            issues.extend(result.get("coherence", {}).get("issues", []))

            if issues:
                lines.append("**💡 Points à améliorer :**")
                for issue in issues:
                    lines.append(f"- {issue}")
                lines.append("")

            lines.append("---\n")

        # Recommandations globales
        lines.extend(
            [
                "## 🎯 Recommandations Globales",
                "",
                "### Priorité Haute",
                "",
                "1. **README** : S'assurer que tous les projets ont un README complet avec :",
                "   - Titre et description claire",
                "   - Badges (version, tests, coverage)",
                "   - Section installation",
                "   - Exemples d'utilisation",
                "",
                "2. **Structure** : Standardiser la structure des projets :",
                "   - Dossier `tests/`",
                "   - Dossier `docs/`",
                "   - CI/CD configuré",
                "   - Docker pour production",
                "",
                "3. **Métriques** : Mentionner dans les descriptions :",
                "   - Nombre de tests",
                "   - Coverage si disponible",
                "   - Version actuelle",
                "",
                "---",
                "",
                "*Rapport généré automatiquement par `scripts/audit-projects.py`*",
            ]
        )

        report = "\n".join(lines)

        if output_file:
            output_file.write_text(report, encoding="utf-8")
            print(f"\n✅ Rapport sauvegardé : {output_file}")

        return report


def main():
    parser = argparse.ArgumentParser(description="🔍 Audit complet des projets Arkalia Luna System")
    parser.add_argument(
        "--output",
        type=str,
        default="audits/AUDIT-COMPLET-PROJETS.md",
        help="Fichier de sortie pour le rapport (défaut: audits/AUDIT-COMPLET-PROJETS.md)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode verbeux")
    parser.add_argument(
        "--data",
        type=str,
        default="config/projects-data.json",
        help="Fichier de données des projets (défaut: config/projects-data.json)",
    )

    args = parser.parse_args()

    script_dir = Path(__file__).parent.parent
    data_file = script_dir / args.data
    output_file = script_dir / args.output

    # Crée le dossier audits s'il n'existe pas
    output_file.parent.mkdir(parents=True, exist_ok=True)

    print("🔍 Arkalia Luna System - Audit Complet des Projets")
    print("=" * 60)

    auditor = ProjectAuditor(data_file)
    results = auditor.audit_all()

    report = auditor.generate_report(results, output_file)

    if args.verbose:
        print("\n" + report)

    print(f"\n✅ Audit terminé : {len(results)} projets analysés")
    print(f"📄 Rapport : {output_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

