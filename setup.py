import ez_setup

ez_setup.use_setuptools()

from setuptools import setup, find_packages

exec(open("bioprinter/version.py").read())  # loads __version__

setup(
    name="bioprinter",
    version=__version__,
    author="Zulko",
    description="",
    long_description=open("pypi-readme.rst").read(),
    license="MIT",
    url="https://github.com/Edinburgh-Genome-Foundry/bioprinter",
    keywords="bioprinter pointillism living art",
    packages=find_packages(exclude="docs"),
    install_requires=["numpy", "Pillow", "pytest"],
)
