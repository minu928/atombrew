from pathlib import Path
from setuptools import setup, find_packages


version_dict = {}
with open(Path(__file__).parents[0] / "atombrew/__version.py") as this_v:
    exec(this_v.read(), version_dict)
version = version_dict["__version__"]
del version_dict


setup(
    name="atombrew",
    version=version,
    author="Knu",
    author_email="minu928@snu.ac.kr",
    url="https://github.com/minu928/atombrew",
    install_requires=["numpy>=1.22.3", "tqdm>=4.66.4", "scipy>=1.11.4", "pandas>=2.1.4"],
    description="Package for post-processing the trajectory files of MD.",
    packages=find_packages(),
    python_requires=">=3.9",
    package_data={"": ["*"]},
    entry_points={
        "console_scripts": [
            "atb = atombrew.cli.__init__:parsing",
        ]
    },
    zip_safe=True,
)
