from setuptools import setup

exec(open('bioprinter/version.py').read())  # loads __version__

setup(name='BioPrinter',
      version=__version__,
      author='Zulko',
      description='',
      long_description=open('README.rst').read(),
      license='see LICENSE.txt',
      keywords="bioprinter pointillism living art",
      packages=['bioprinter'],
      install_requires=['numpy', 'Pillow', 'pytest'])
