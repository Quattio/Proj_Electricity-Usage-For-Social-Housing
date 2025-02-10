from setuptools import find_packages, setup

setup(
    name="project",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "pandas",
        "sklearn",
        "scipy"
    ],
    extras_require={"dev": ["flake8", "pytest"]},
)
