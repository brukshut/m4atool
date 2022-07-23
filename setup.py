import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="m4atool",
    version="0.0.1",
    author="Christian Gough",
    author_email="christian@gturn.xyz",
    description=("An tool for manipulating Apple Lossless files."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brukshut/m4atool",
    project_urls={
        "Bug Tracker": "https://github.com/brukshut/m4atool/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["mutagen"],
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "m4atool = m4atool.cli:main",
        ]
    }
)
