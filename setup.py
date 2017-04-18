from setuptools import setup


setup(
    name='polygraph',
    version='0.1.0',
    description='Python library for defining GraphQL schemas',
    url='https://github.com/polygraph-python/polygraph',
    author='Wei Yen, Lee',
    author_email='hello@weiyen.net',
    license='MIT',
    install_requires=[
        'graphql-core>=1.0.1',
    ],
    extras_require={
        'dev': [
            'flake8',
            'ipython',
            'autopep8',
            'isort',
            'pudb==2017.1.2',
            'twine==1.8.1',
            'coverage',
            'virtualenvwrapper',
        ],
        'test': [
            'isort',
            'coverage',
            'coveralls',
        ]
    }
)
