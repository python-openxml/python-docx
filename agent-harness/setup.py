from pathlib import Path

from setuptools import find_namespace_packages, setup

BASE_DIR = Path(__file__).parent
README = (BASE_DIR / "cli_anything" / "python_docx" / "README.md").read_text(encoding="utf-8")

setup(
    name="cli-anything-python-docx",
    version="0.1.0",
    description="CLI-Anything harness for python-docx",
    long_description=README,
    long_description_content_type="text/markdown",
    author="CLI-Anything",
    packages=find_namespace_packages(include=["cli_anything.*"]),
    include_package_data=True,
    install_requires=[
        "click>=8.1.7",
        "python-docx>=1.1.2",
    ],
    extras_require={
        "dev": ["pytest>=7.4.0"],
    },
    entry_points={
        "console_scripts": [
            "cli-anything-python-docx=cli_anything.python_docx.__main__:main",
        ],
    },
    python_requires=">=3.9",
)