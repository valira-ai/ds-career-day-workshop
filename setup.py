from setuptools import find_packages, setup

setup(
    name="airbnb_model",
    version="0.0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src", include=["airbnb_model", "airbnb_model/*"]),
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
)
