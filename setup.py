"""Setup script for Celestial Engine."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="celestial-engine",
    version="2.0.0",
    author="Celestial Engine Team",
    description="Advanced theological entry generation system for CELESTIAL-tier Orthodox Christian content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/celestial-engine",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Religion",
        "Topic :: Religion",
        "Topic :: Text Processing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "pyyaml>=6.0",
        "requests>=2.31.0",
        "click>=8.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "celestial=celestial_engine.cli.main:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "celestial_engine": ["config/*.yaml"],
    },
)
