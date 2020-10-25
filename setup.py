from setuptools import setup

setup(
    name = 'bigbang',
    version = '0.1.0',
    packages = ['bigbang'],
    entry_points = {
        'console_scripts': [
            'bigbang = bigbang.__main__:main'
        ]
    })