from setuptools import setup, find_packages

setup(
    name='cli_devops',
    version='0.1.0',
    # py_modules=['cli_devops'],
    # packages=find_packages(),
    install_requires=[
        'Click',
        'requests',
        'tabulate'
    ],
    entry_points={
        'console_scripts': [
            'cli_devops = cli_devops.main:cli',
        ],
    },
)
