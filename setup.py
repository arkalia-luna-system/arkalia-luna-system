#!/usr/bin/env python3
"""Setup script for github-profile-arkalia"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="github-profile-arkalia",
    version="1.0.0",
    description="🌙 Système de gestion automatique du profil GitHub Arkalia Luna System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Arkalia Luna System",
    author_email="arkalia.luna.system@gmail.com",
    url="https://github.com/arkalia-luna-system/arkalia-luna-system",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=[
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=23.0",
            "ruff>=0.1.0",
            "mypy>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "update-profile=github_profile.core.updater:main",
            "generate-sections=github_profile.generators.sections:main",
            "auto-update=github_profile.core.auto_update:main",
            "transform-professional=github_profile.transformers.professional:main",
            "optimize-performance=github_profile.transformers.performance:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Documentation",
    ],
    keywords="github profile automation readme arkalia",
)

