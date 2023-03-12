from setuptools import setup, find_packages

setup(
    name='cli_devops',
    version='0.1.0',
    setup_requires=['flake8', 'pytest-runner',],
    install_requires=[
        'Click',
        'requests',
        'tabulate',
        'pytest', 'requests-mock'
    ],
    entry_points={
        'console_scripts': [
            'cli_devops = cli_devops.main:cli',
        ],
    },
)
