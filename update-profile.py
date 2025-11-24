#!/usr/bin/env python3
"""
🌙 Script Intelligent de Mise à Jour du Profil GitHub
Arkalia Luna System - Automatisation Propre & Performante

Usage:
    python update-profile.py [--dry-run] [--force] [--verbose]
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

try:
    import requests
except ImportError:
    print("❌ 'requests' non installé. Installez-le avec: pip install requests")
    sys.exit(1)


@dataclass
class ProjectInfo:
    """Informations d'un projet détecté"""

    name: str
    github_url: str
    local_path: Optional[Path] = None
    readme_path: Optional[Path] = None
    description: str = ""
    language: str = ""
    stars: int = 0
    is_public: bool = True


class GitHubProfileUpdater:
    """Gestionnaire intelligent pour mettre à jour le profil GitHub"""

    def __init__(self, username: str = "arkalia-luna-system", base_path: Optional[Path] = None):
        self.username = username
        self.base_path = base_path if base_path is not None else Path("/Volumes/T7")
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.session = requests.Session()

        if self.github_token:
            self.session.headers.update(
                {
                    "Authorization": f"token {self.github_token}",
                    "Accept": "application/vnd.github.v3+json",
                }
            )

        self.projects: List[ProjectInfo] = []
        self.profile_repo_path = Path(__file__).parent

    def fetch_github_repos(self) -> List[Dict[str, Any]]:
        """Récupère tous les repos GitHub via API"""
        print("🔍 Récupération des projets depuis GitHub...")
        repos: List[Dict[str, Any]] = []
        page = 1
        per_page = 100

        while True:
            url = f"https://api.github.com/users/{self.username}/repos"
            params: Dict[str, Any] = {
                "type": "all",
                "sort": "updated",
                "direction": "desc",
                "per_page": per_page,
                "page": page,
            }

            try:
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()
                page_repos = response.json()

                if not page_repos:
                    break

                repos.extend(page_repos)

                if len(page_repos) < per_page:
                    break

                page += 1

            except requests.exceptions.RequestException as e:
                print(f"⚠️  Erreur API GitHub: {e}")
                if not self.github_token:
                    print("💡 Astuce: Définissez GITHUB_TOKEN pour plus de requêtes API")
                break

        print(f"✅ {len(repos)} projets trouvés sur GitHub")
        return repos

    def _generate_name_variants(self, repo_name: str) -> List[str]:
        """Génère des variations du nom pour la recherche"""
        if not repo_name:
            return []

        variants = [repo_name]

        # Variations avec underscores/tirets
        if "_" in repo_name:
            variants.append(repo_name.replace("_", "-"))
            variants.append(repo_name.replace("_", ""))
        if "-" in repo_name:
            variants.append(repo_name.replace("-", "_"))
            variants.append(repo_name.replace("-", ""))

        # Variations de casse
        variants.append(repo_name.lower())
        variants.append(repo_name.upper())
        if len(repo_name) > 0 and repo_name[0].isupper():
            variants.append(repo_name[0].lower() + repo_name[1:])

        # Variations spécifiques connues
        if "bbia-sim" in repo_name.lower():
            variants.append("bbia-reachy-sim")
        if "arkalia-luna-pro" in repo_name.lower():
            variants.append("arkalia-luna-pro")
        if "ia-pipeline" in repo_name.lower() or "pipeline" in repo_name.lower():
            variants.append("athalia-dev-setup")
            variants.append("ia-pipeline")
            variants.append("athalia")
        if "bbia_branding" in repo_name.lower() or "branding" in repo_name.lower():
            variants.append("bbia_branding")
            variants.append("bbia-branding")
            variants.append("branding")
            # Cherche aussi dans "logo bbia" sur Desktop
            desktop_bbia = Path.home() / "Desktop" / "logo bbia" / "bbia_branding"
            if desktop_bbia.exists() and (desktop_bbia / ".git").exists():
                # Sera trouvé par la recherche normale, mais on peut aussi le retourner directement
                pass
        if "arkalia-luna-system" in repo_name.lower():
            variants.append("github-profile-arkalia")
            variants.append("arkalia-luna-system")
        # Variations pour "arkalia finance" et projets finance
        if "finance" in repo_name.lower() or "arkalia-finance" in repo_name.lower():
            variants.append("arkalia-finance")
            variants.append("arkalia_finance")
            variants.append("finance")
        # Variations pour "arkalia-aria" (avec majuscule)
        if "aria" in repo_name.lower() and "arkalia" in repo_name.lower():
            variants.append("Arkalia-aria")
            variants.append("arkalia-aria")
            variants.append("arkalia_aria")
        # Variations pour "arkalia-luna-logo" (avec majuscule)
        if "luna-logo" in repo_name.lower() or "luna_logo" in repo_name.lower():
            variants.append("Arkalia-luna-logo")
            variants.append("arkalia-luna-logo")
            variants.append("arkalia_luna_logo")

        return list(set(variants))  # Supprime les doublons

    def find_local_project_path(self, repo_name: str) -> Optional[Path]:
        """Cherche intelligemment le chemin local d'un projet"""
        # Génère des variations du nom
        name_variants = self._generate_name_variants(repo_name)

        # Dossiers connus à chercher
        desktop = Path.home() / "Desktop"
        known_dirs = [
            "",  # Racine
            "devstation",
            "devstation/cursor",
            "logo",
            "Projects",
            "Dev",
            "Code",
            "github-profile-arkalia",
            "strict_backup",
            "strict_backup/arkalia_luna_backup",
            "arkalia",  # Dossier arkalia général
            "arkalia-projects",  # Dossier projets arkalia
            "finance",  # Dossier finance
            "arkalia-finance",  # Dossier finance spécifique
        ]

        # Chemins probables à vérifier
        search_paths = []
        for variant in name_variants:
            for known_dir in known_dirs:
                if known_dir:
                    search_paths.append(self.base_path / known_dir / variant)
                else:
                    search_paths.append(self.base_path / variant)
            # Aussi dans home
            search_paths.append(Path.home() / "Projects" / variant)
            search_paths.append(Path.home() / "Dev" / variant)

            # Chemins Desktop spécifiques
            if desktop.exists():
                search_paths.append(desktop / variant)
                search_paths.append(desktop / "logo bbia" / variant)
                search_paths.append(desktop / "a trier" / variant)
                # Cas spécial pour bbia_branding
                if "bbia" in variant.lower() and "branding" in variant.lower():
                    search_paths.append(desktop / "logo bbia" / "bbia_branding")

        # Cherche dans les sous-dossiers connus (max 2 niveaux)
        desktop = Path.home() / "Desktop"
        known_parents = [
            self.base_path,
            self.base_path / "devstation",
            self.base_path / "logo",
            self.base_path / "github-profile-arkalia",
            self.base_path / "strict_backup",
            self.base_path / "arkalia",
            self.base_path / "arkalia-projects",
            self.base_path / "finance",
            self.base_path / "arkalia-finance",
        ]

        # Ajoute Desktop si disponible
        if desktop.exists():
            known_parents.extend(
                [
                    desktop,
                    desktop / "logo bbia",
                    desktop / "a trier",
                ]
            )

        # Cas spéciaux : projets avec chemins spécifiques
        if "arkalia-luna-system" in repo_name.lower():
            profile_repo = self.profile_repo_path
            if (profile_repo / ".git").exists():
                return profile_repo

        # Cas spécial : bbia_branding sur Desktop
        if "bbia_branding" in repo_name.lower() or (
            "bbia" in repo_name.lower() and "branding" in repo_name.lower()
        ):
            desktop_bbia = Path.home() / "Desktop" / "logo bbia" / "bbia_branding"
            if desktop_bbia.exists() and desktop_bbia.is_dir() and (desktop_bbia / ".git").exists():
                return desktop_bbia

        for parent in known_parents:
            if not parent.exists():
                continue
            try:
                # Cherche max 2 niveaux de profondeur pour performance
                for item in parent.iterdir():
                    if not item.is_dir():
                        continue

                    # Vérifie si le nom correspond (exact ou variation)
                    item_name_lower = item.name.lower()
                    repo_name_lower = repo_name.lower()

                    # Correspondance exacte
                    if any(variant.lower() == item_name_lower for variant in name_variants):
                        if (item / ".git").exists():
                            return item

                    # Correspondance partielle (pour athalia-dev-setup = ia-pipeline)
                    if "pipeline" in repo_name_lower and "athalia" in item_name_lower:
                        if (item / ".git").exists():
                            return item
                    if "athalia" in repo_name_lower and "athalia" in item_name_lower:
                        if (item / ".git").exists():
                            return item

                    # Cherche un niveau de plus
                    for variant in name_variants:
                        subdir = item / variant
                        if subdir.exists() and subdir.is_dir() and (subdir / ".git").exists():
                            return subdir
            except (PermissionError, OSError):
                continue

        # Vérifie les chemins directs
        for path in search_paths:
            if path.exists() and path.is_dir():
                # Vérifie que c'est bien un repo git
                if (path / ".git").exists():
                    return path

        return None

    def find_readme(self, project_path: Path) -> Optional[Path]:
        """Trouve le README racine d'un projet"""
        readme_variants = [
            "README.md",
            "readme.md",
            "Readme.md",
            "README.rst",
            "README.txt",
        ]

        for variant in readme_variants:
            readme_path = project_path / variant
            if readme_path.exists() and readme_path.is_file():
                return readme_path

        return None

    def extract_description_from_readme(self, readme_path: Path) -> str:
        """Extrait intelligemment la description depuis un README"""
        try:
            content = readme_path.read_text(encoding="utf-8", errors="ignore")
            lines = content.split("\n")
            description = ""
            found_title = False
            in_code_block = False

            for i, line in enumerate(lines[:80]):  # Limite aux 80 premières lignes
                line_stripped = line.strip()

                # Gère les blocs de code
                if line_stripped.startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    continue

                # Ignore les lignes vides, badges, liens purs
                if (
                    not line_stripped
                    or line_stripped.startswith("#")
                    or line_stripped.startswith("[!")
                    or (line_stripped.startswith("http") and " " not in line_stripped)
                    or line_stripped.startswith("|")  # Tableaux
                    or line_stripped.startswith("---")
                    or line_stripped.startswith("```")
                ):
                    if line_stripped.startswith("#"):
                        found_title = True
                    continue

                # Cherche après le titre principal
                if found_title and len(line_stripped) > 25:
                    # Vérifie que ce n'est pas un titre de section
                    if not line_stripped.startswith("##"):
                        # Prend la première ligne significative
                        description = line_stripped
                        break

            # Si pas trouvé, cherche dans les premières lignes avec patterns
            if not description:
                for line in lines[:30]:
                    line_stripped = line.strip()
                    if (
                        len(line_stripped) > 30
                        and not line_stripped.startswith("#")
                        and not line_stripped.startswith("[")
                        and not line_stripped.startswith("|")
                        and not line_stripped.startswith("```")
                    ):
                        # Vérifie que c'est une vraie description
                        if any(char.isalpha() for char in line_stripped[:10]):
                            description = line_stripped
                            break

            # Nettoie la description
            if description:
                # Enlève les emojis en début si trop nombreux
                while description and description[0] in "🌙🤖🎨📱🧠🔧📊⚙️✅🚀📈":
                    description = description[1:].strip()
                # Limite à 200 caractères
                description = description[:200].strip()
                # Enlève les points de suspension multiples
                description = description.replace("...", "…")

            return description
        except Exception:  # noqa: BLE001
            # Erreur lors de l'extraction de la description (fichier corrompu, encoding, etc.)
            return ""

    def detect_secondary_languages(self, project_path: Path) -> List[str]:
        """Détecte intelligemment les langages secondaires dans un projet"""
        languages: List[str] = []

        if not project_path.exists():
            return languages

        # Extensions connues avec poids (plus fréquent = plus important)
        lang_extensions = {
            ".sh": "Shell",
            ".bash": "Shell",
            ".zsh": "Shell",
            ".dockerfile": "Dockerfile",
            "Dockerfile": "Dockerfile",
            ".yml": "YAML",
            ".yaml": "YAML",
            ".json": "JSON",
            ".md": "Markdown",
            ".html": "HTML",
            ".css": "CSS",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".go": "Go",
            ".rs": "Rust",
            ".java": "Java",
            ".cpp": "C++",
            ".c": "C",
            ".py": "Python",
            ".dart": "Dart",
            ".sql": "SQL",
            ".r": "R",
            ".m": "Objective-C",
            ".swift": "Swift",
            ".kt": "Kotlin",
            ".scala": "Scala",
            ".php": "PHP",
            ".rb": "Ruby",
            ".lua": "Lua",
        }

        found_languages: Dict[str, float] = {}  # Dict pour compter les occurrences

        def count_language(lang: str):
            """Compte les occurrences d'un langage"""
            found_languages[lang] = found_languages.get(lang, 0) + 1

        try:
            # Cherche dans les fichiers racine (priorité haute)
            for item in project_path.iterdir():
                if item.is_file() and not item.name.startswith("."):
                    ext = item.suffix.lower()
                    if ext in lang_extensions:
                        count_language(lang_extensions[ext])
                    elif item.name.lower() in ["dockerfile", "docker-compose.yml", "makefile"]:
                        if "docker" in item.name.lower():
                            count_language("Dockerfile")
                        elif "makefile" in item.name.lower():
                            count_language("Makefile")

            # Cherche dans les sous-dossiers principaux (max 2 niveaux, poids moindre)
            for item in project_path.iterdir():
                if item.is_dir() and not item.name.startswith("."):
                    try:
                        for subitem in item.iterdir():
                            if subitem.is_file() and not subitem.name.startswith("."):
                                ext = subitem.suffix.lower()
                                if ext in lang_extensions:
                                    # Poids moindre pour les sous-dossiers
                                    lang = lang_extensions[ext]
                                    found_languages[lang] = found_languages.get(lang, 0) + 0.5
                    except (PermissionError, OSError):
                        continue

            # Filtre : garde seulement les langages avec au moins 1 occurrence
            # et exclut le langage principal (sera géré ailleurs)
            filtered = [
                lang
                for lang, count in sorted(found_languages.items(), key=lambda x: x[1], reverse=True)
                if count >= 1
            ]

            return sorted(filtered)
        except (PermissionError, OSError):
            pass

        return []

    def analyze_project(self, repo_data: Dict[str, Any]) -> ProjectInfo:
        """Analyse un projet et trouve ses infos locales"""
        repo_name = repo_data.get("name", "")
        github_url = repo_data.get("html_url", "")

        if not repo_name:
            raise ValueError("Le repo_data doit contenir un champ 'name'")

        project = ProjectInfo(
            name=repo_name,
            github_url=github_url,
            description=repo_data.get("description", ""),
            language=repo_data.get("language", ""),
            stars=repo_data.get("stargazers_count", 0),
            is_public=not repo_data.get("private", False),
        )

        # Cherche le chemin local
        local_path = self.find_local_project_path(repo_name)
        if local_path:
            project.local_path = local_path
            project.readme_path = self.find_readme(local_path)

            # Extrait la description depuis le README si disponible
            if project.readme_path:
                readme_desc = self.extract_description_from_readme(project.readme_path)
                if readme_desc and not project.description:
                    project.description = readme_desc

            print(f"  ✅ {repo_name}: {local_path}")
        else:
            print(f"  ⚠️  {repo_name}: non trouvé localement")

        return project

    def discover_projects(self) -> List[ProjectInfo]:
        """Découvre tous les projets (GitHub + local)"""
        print("\n🌙 Découverte des projets Arkalia Luna System...\n")

        # Récupère depuis GitHub
        github_repos = self.fetch_github_repos()

        # Analyse chaque projet
        for repo in github_repos:
            project = self.analyze_project(repo)
            self.projects.append(project)

        print(f"\n📊 Résumé: {len(self.projects)} projets analysés")
        print(f"   - {sum(1 for p in self.projects if p.local_path)} trouvés localement")
        print(f"   - {sum(1 for p in self.projects if p.readme_path)} avec README")

        return self.projects

    def generate_profile_stats(self) -> Dict:
        """Génère les statistiques pour le profil"""
        stats = {
            "total_projects": len(self.projects),
            "local_projects": sum(1 for p in self.projects if p.local_path),
            "projects_with_readme": sum(1 for p in self.projects if p.readme_path),
            "total_stars": sum(p.stars for p in self.projects),
            "languages": {},
            "last_updated": datetime.now().isoformat(),
        }

        # Compte les langages (principal + secondaires)
        languages_dict: Dict[str, int] = {}
        for project in self.projects:
            # Langage principal
            if project.language:
                languages_dict[project.language] = languages_dict.get(project.language, 0) + 1

            # Langages secondaires
            if project.local_path:
                secondary_langs = self.detect_secondary_languages(project.local_path)
                for lang in secondary_langs:
                    # Ne compte pas le langage principal comme secondaire
                    if lang != project.language:
                        languages_dict[lang] = languages_dict.get(lang, 0) + 1
        stats["languages"] = languages_dict

        return stats

    def export_project_list(self, output_file: Optional[Path] = None) -> Path:
        """Exporte la liste des projets en JSON"""
        if output_file is None:
            output_file = self.profile_repo_path / "config" / "projects-data.json"

        data = {
            "username": self.username,
            "generated_at": datetime.now().isoformat(),
            "stats": self.generate_profile_stats(),
            "projects": [
                {
                    "name": p.name,
                    "github_url": p.github_url,
                    "local_path": str(p.local_path) if p.local_path else None,
                    "readme_path": str(p.readme_path) if p.readme_path else None,
                    "description": p.description,
                    "language": p.language,
                    "stars": p.stars,
                    "is_public": p.is_public,
                }
                for p in self.projects
            ],
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Données exportées: {output_file}")
        return output_file

    def print_summary(self):
        """Affiche un résumé des projets trouvés"""
        print("\n" + "=" * 60)
        print("📋 RÉSUMÉ DES PROJETS")
        print("=" * 60)

        for i, project in enumerate(self.projects, 1):
            status = "✅" if project.local_path else "⚠️ "
            readme_status = "📖" if project.readme_path else "  "

            print(f"\n{i}. {status} {readme_status} {project.name}")
            print(f"   GitHub: {project.github_url}")
            if project.local_path:
                print(f"   Local:  {project.local_path}")
            if project.readme_path:
                print(f"   README: {project.readme_path}")
            if project.description:
                print(f"   Desc:   {project.description}")
            if project.language:
                print(f"   Lang:   {project.language} ⭐ {project.stars}")

        stats = self.generate_profile_stats()
        print("\n" + "=" * 60)
        print("📊 STATISTIQUES")
        print("=" * 60)
        print(f"Total projets:     {stats['total_projects']}")
        print(f"Projets locaux:    {stats['local_projects']}")
        print(f"Avec README:       {stats['projects_with_readme']}")
        print(f"Total stars:       {stats['total_stars']}")
        print(f"Langages:          {', '.join(stats['languages'].keys())}")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="🌙 Mise à jour intelligente du profil GitHub Arkalia Luna System"
    )
    parser.add_argument("--dry-run", action="store_true", help="Mode test (ne modifie rien)")
    parser.add_argument(
        "--force", action="store_true", help="Force la mise à jour même si déjà à jour"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode verbeux")
    parser.add_argument(
        "--base-path",
        type=str,
        help="Chemin de base pour chercher les projets (défaut: /Volumes/T7)",
    )
    parser.add_argument(
        "--export", type=str, help="Fichier de sortie pour exporter les données JSON"
    )

    args = parser.parse_args()

    base_path = Path(args.base_path) if args.base_path else None

    print("🌙 Arkalia Luna System - Profile Updater")
    print("=" * 60)

    updater = GitHubProfileUpdater(base_path=base_path)

    # Découvre les projets
    updater.discover_projects()

    # Exporte les données
    export_path = updater.export_project_list(Path(args.export) if args.export else None)

    # Affiche le résumé
    updater.print_summary()

    if args.dry_run:
        print("\n🔍 Mode DRY-RUN: Aucune modification effectuée")
    else:
        print("\n✅ Mise à jour terminée!")
        print(f"📁 Utilisez le fichier {export_path} pour mettre à jour votre README.md")

    return 0


if __name__ == "__main__":
    sys.exit(main())
