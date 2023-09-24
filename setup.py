from setuptools import setup

setup(
    name='pbj',
    version='0.1.0',
    py_modules=['main','pbj','deck','player','extend_click'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'pbj = main:cli',
        ],
    },
)