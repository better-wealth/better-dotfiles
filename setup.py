"""Setup."""
import os
import pathlib
import re
from typing import List

from setuptools import find_packages
from setuptools import setup


REGEXP = re.compile(r'^__version__\W*=\W*"([\d.abrc]+)"')
PARENT = pathlib.Path(__file__).parent


def read_version():
    """read_version."""
    init_py = os.path.join(
        os.path.dirname(__file__), "src", "better_dotfiles", "__init__.py"
    )

    with open(init_py, encoding="utf-8") as open_file:
        for line in open_file:
            match = REGEXP.match(line)
            if match is not None:
                return match.group(1)
        msg = f"Cannot find version in ${init_py}"
        raise RuntimeError(msg)


def read_requirements(path: str) -> List[str]:
    """read_requirements."""
    file_path = PARENT / path
    with open(file_path, encoding="utf-8") as open_file:
        return open_file.read().split("\n")


if __name__ == "__main__":
    setup(
        name="better_dotfiles",
        version=read_version(),
        description="Better dotfiles management tools.",
        platforms=["POSIX"],
        packages=find_packages(),
        package_data={"": ["config/*.*"]},
        include_package_data=True,
        install_requires=read_requirements("requirements/production.txt"),
        zip_safe=False,
        entry_points={
            "console_scripts": [
                "cli-name = better_dotfiles.better_dotfiles:trending_homebrew"
            ]
        },
    )
