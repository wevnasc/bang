from setuptools import setup

setup(
    name = 'bang',
    version = '0.1.0',
    packages = ['bang'],
    entry_points = {
        'console_scripts': [
            'bang = bang.__main__:main'
        ]
    })