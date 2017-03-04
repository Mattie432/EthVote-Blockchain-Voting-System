from setuptools import setup

setup(
    name='ApplicationServer',
    version='1.0.0',
    author='Mattie432',
    author_email='matt@mattie432.com',
    description='',
    url='https://github.com/Mattie432/Blockchain-Voting-System',
    packages=[
        'ApplicationServer_FrontEnd',
        'ApplicationServer_BackEnd'
    ],
    install_requires=[
        'Django'
    ]
)
