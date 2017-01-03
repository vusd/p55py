from setuptools import setup
from setuptools import find_packages

install_requires = [
    'Pillow'
]

setup(name='p55py',
      version='0.2.0',
      description='Experimental python based Creative Coding library',
      author='Tom White',
      author_email='tom@sixdozen.com',
      url='https://github.com/vusd/p55py',
      download_url='https://github.com/vusd/p55py/archive/0.2.0.tar.gz',
      license='MIT',
      entry_points={
      },
      install_requires=install_requires,
      packages=find_packages())
