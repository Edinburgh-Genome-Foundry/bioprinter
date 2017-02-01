import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

exec(open('bioprinter/version.py').read())  # loads __version__

setup(name='BioPrinter',
      version=__version__,
      author='Zulko',
      description='',
      long_description=open('README.rst').read(),
      license='see LICENSE.txt',
      keywords="bioprinter pointillism living art",
      packages=find_packages(exclude='docs'),
      install_requires=['numpy', 'scikit-image', 'pytest'])
