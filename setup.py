"""
LitZentrum - Setup Script
"""
from setuptools import setup, find_packages
from pathlib import Path

# README laden
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="litzentrum",
    version="1.0.0",
    author="LitZentrum Team",
    description="Ordnerbasierte Literaturverwaltung",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/litzentrum/litzentrum",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "PyQt6>=6.4.0",
        "PyMuPDF>=1.23.0",
        "bibtexparser>=1.4.0",
        "jsonschema>=4.17.0",
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-qt>=4.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "litzentrum=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Text Processing :: Linguistic",
    ],
    keywords="literature management, bibliography, research, citation",
)
