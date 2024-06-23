from pathlib import Path
from setuptools import setup, find_packages


version_dict = {}
with open(Path(__file__).parents[0] / "atombrew/__version__.py") as this_v:
    exec(this_v.read(), version_dict)
version = version_dict["__version__"]
del version_dict


setup(
    name="mdbrew",
    version=version,
    author="Knu",
    author_email="minu928@snu.ac.kr",
    url="https://github.com/minu928/atombrew",
    install_requies=[
        "numpy>=1.21.0",
        "pandas>=2.1.4",
        "tqdm>=4.66.4",
        "scipy>=1.11.4",
    ],
    description="Package for post-processing the trajectory files of MD.",
    packages=find_packages(),
    python_requires=">=3.9",
    package_data={"": ["*"]},
    zip_safe=True,
)
