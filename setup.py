from setuptools import setup, find_packages

setup(
    name="mycli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],  # Add click or other dependencies if needed
    entry_points={
        "console_scripts": [
            "Robot2DStudio=Template.CLI:main",
        ],
    },
)