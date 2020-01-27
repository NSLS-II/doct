from setuptools import setup

setup(
    name='doct',
    version='1.1.0',
    author='Brookhaven National Laboratory',
    license='BSD 3-Clause',
    py_modules=['doct'],
    description='A read-only dottable dictionary',
    url='http://github.com/NSLS-II/doct',
    install_requires=['humanize', 'prettytable'],
    python_requires='>=3.6'
)
