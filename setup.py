from setuptools import setup


setup(
    name='polygraph',
    version='0.1.0',
    description='Python library for defining GraphQL schemas',
    url='https://github.com/yen223/polygraph/',
    author='Wei Yen, Lee',
    author_email='hello@weiyen.net',
    license='MIT',
    install_requires=[
        'marshmallow>=3.0.0b2',
        'graphql-core>=1.0.1',
    ],
    extras_require={
        'dev': [
            'flake8',
            'ipython',
            'autopep8',
        ]
    }
)