# coding=utf-8
from distutils.core import setup

setup(
    name='BioREST',
    version='1.0',
    packages=['BioREST'],
    install_requires=['requests', 'beautifulsoup4'],
    url='https://github.com/ArnaudKOPP/BioREST',
    license='GNU GPL V2.0',
    author='Arnaud KOPP',
    author_email='kopp.arnaud@gmail.com',
    description='Data retrieving of biological database using REST api'
)