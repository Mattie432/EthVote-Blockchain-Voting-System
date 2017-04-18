from setuptools import setup

setup(
    name='externalvoterregistration',
    version='1.0.0',
    author='Mattie432',
    author_email='matt@mattie432.com',
    description='',
    url='https://github.com/Mattie432/Blockchain-Voting-System',
    packages=[
        'externalvoterregistration'
    ],
    install_requires=[
        'Django>=1.10.0',
        'psycopg2',
        'crochet',
        'twisted',
        'uwsgi'
    ]
)
