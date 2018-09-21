from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='eggit',
    version='0.0.22',
    description='a python lib',
    long_description=long_description,
    author='JoiT',
    author_email='myjoit@outlook.com',
    url='https://github.com/MyJoiT/eggit',
    download_url='https://github.com/MyJoiT/eggit/archive/0.0.22.tar.gz',
    packages=find_packages(exclude=[]),
    keywords=('eggit, lib, tool'),
    install_requires=[
        'pyjwt>=1.4.2',
        'sqlalchemy>=1.2.7',
        'flask-restful>=0.3.6'
        ],
    license='GPL3',
    zip_safe=True
)
