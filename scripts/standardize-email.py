#!/usr/bin/env python3
"""
🌙 Script de Standardisation Email - Arkalia Luna System
Remplace toutes les adresses email par arkalia.luna.system@gmail.com

Usage:
    python scripts/standardize-email.py [--dry-run] [--repo-path PATH]
"""

import re
import os
import sys
import argparse
from pathlib import Path
from typing import List, Tuple

# Email cible
TARGET_EMAIL = "arkalia.luna.system@gmail.com"
CORRECT_NAME = "Athalia Siwek"

# Extensions à traiter
EXTENSIONS = {
    ".md", ".py", ".js", ".ts", ".json", ".yml", ".yaml", 
    ".toml", ".txt", ".env", ".sh", ".bash"
}

# Fichiers spéciaux
SPECIAL_FILES = {"LICENSE", "CONTRIBUTING.md", "CONTRIBUTING.txt"}

# Dossiers à ignorer
IGNORE_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", 
    ".pytest_cache", ".mypy_cache", "dist", "build", ".tox"
}


def find_email_patterns(content: str) -> List[Tuple[str, int]]:
    """Trouve tous les emails dans le contenu"""
    # Pattern pour emails (évite de matcher le target email)
    pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
    matches = []
    
    for match in re.finditer(pattern, content):
        email = match.group(0)
        if email.lower() != TARGET_EMAIL.lower():
            matches.append((email, match.start()))
    
    return matches


def should_process_file(file_path: Path) -> bool:
    """Vérifie si un fichier doit être traité"""
    # Ignorer les fichiers dans les dossiers à ignorer
    for part in file_path.parts:
        if part in IGNORE_DIRS:
            return False
    
    # Vérifier l'extension
    if file_path.suffix.lower() in EXTENSIONS:
        return True
    
    # Vérifier les fichiers spéciaux
    if file_path.name in SPECIAL_FILES:
        return True
    
    return False


def replace_emails_in_file(file_path: Path, dry_run: bool = False) -> Tuple[int, int]:
    """
    Remplace les emails dans un fichier
    Retourne (nombre_emails_trouvés, nombre_remplacés)
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        print(f"   ⚠️  Erreur lecture {file_path}: {e}")
        return (0, 0)
    
    # Trouver les emails
    emails = find_email_patterns(content)
    
    if not emails:
        return (0, 0)
    
    # Remplacer
    new_content = content
    replacements = 0
    
    for email, _ in emails:
        # Remplacer toutes les occurrences de cet email
        pattern = re.escape(email)
        new_content = re.sub(pattern, TARGET_EMAIL, new_content)
        replacements += 1
    
    # Écrire si pas dry-run
    if not dry_run and new_content != content:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
        except Exception as e:
            print(f"   ⚠️  Erreur écriture {file_path}: {e}")
            return (len(emails), 0)
    
    return (len(emails), replacements)


def configure_git(repo_path: Path, dry_run: bool = False):
    """Configure git user.email et user.name"""
    if dry_run:
        print("   [DRY-RUN] git config user.email =", TARGET_EMAIL)
        print("   [DRY-RUN] git config user.name =", CORRECT_NAME)
        return
    
    import subprocess
    
    try:
        subprocess.run(
            ["git", "config", "user.email", TARGET_EMAIL],
            cwd=repo_path,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "config", "user.name", CORRECT_NAME],
            cwd=repo_path,
            check=True,
            capture_output=True
        )
        print(f"   ✅ git config user.email = {TARGET_EMAIL}")
        print(f"   ✅ git config user.name = {CORRECT_NAME}")
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️  Erreur config git: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="🌙 Standardisation Email - Arkalia Luna System"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mode test (ne modifie rien)"
    )
    parser.add_argument(
        "--repo-path",
        type=str,
        default=".",
        help="Chemin du repository (défaut: répertoire courant)"
    )
    
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path).resolve()
    
    # Vérifier qu'on est dans un repo git
    if not (repo_path / ".git").exists():
        print("❌ Erreur : Ce script doit être exécuté dans un repository Git")
        return 1
    
    print("🌙 Standardisation Email - Arkalia Luna System")
    print("=" * 50)
    print("")
    
    if args.dry_run:
        print("🔍 Mode DRY-RUN (aucune modification)")
        print("")
    
    # Demander confirmation si pas dry-run
    if not args.dry_run:
        print("⚠️  Ce script va :")
        print("   1. Remplacer toutes les adresses email dans les fichiers")
        print("   2. Configurer git user.email localement")
        print("")
        response = input("Continuer ? (y/N) ")
        if response.lower() != "y":
            print("❌ Annulé")
            return 0
    
    print("")
    print("🔍 Recherche des fichiers contenant des emails...")
    print("")
    
    files_modified = 0
    emails_found = 0
    emails_replaced = 0
    
    # Parcourir tous les fichiers
    for root, dirs, files in os.walk(repo_path):
        # Ignorer les dossiers à ignorer
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            file_path = Path(root) / file
            
            if should_process_file(file_path):
                found, replaced = replace_emails_in_file(file_path, args.dry_run)
                
                if found > 0:
                    files_modified += 1
                    emails_found += found
                    emails_replaced += replaced
                    
                    status = "[DRY-RUN] " if args.dry_run else ""
                    print(f"   {status}✅ {file_path.relative_to(repo_path)} ({found} email(s))")
    
    print("")
    print("📧 Configuration Git...")
    print("")
    configure_git(repo_path, args.dry_run)
    
    print("")
    print("✅ Standardisation terminée !")
    print("")
    print("📊 Résumé :")
    print(f"   - Fichiers modifiés : {files_modified}")
    print(f"   - Emails trouvés : {emails_found}")
    print(f"   - Emails remplacés : {emails_replaced}")
    print("")
    
    if not args.dry_run:
        print("📝 Prochaines étapes :")
        print("   1. Vérifier les changements : git diff")
        print(f"   2. Commit : git add . && git commit -m '📧 Standardisation email : {TARGET_EMAIL}'")
        print("   3. Push : git push")
        print("")
        print("⚠️  Note : Pour modifier l'historique Git (anciens commits),")
        print("   consultez PLAN-ACTION-1-MOIS.md section 'Standardisation Email'")
        print("")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

