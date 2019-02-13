from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='eggit',
    version='0.0.26',
    description='a python lib',
    long_description=long_description,
    author='JoiT',
    author_email='myjoit@outlook.com',
    url='https://github.com/MyJoiT/eggit',
    packages=find_packages(exclude=[]),
    keywords=('eggit, lib, tool'),
    install_requires=[],
    license='GPL3',
    zip_safe=True
)
