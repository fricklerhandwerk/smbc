from distutils.core import setup
setup(
    name='scripts',
    version='0',
    py_modules=['scrape', 'verify', 'download', 'latest'],
    entry_points={
        'console_scripts': [
            'scrape=scrape:main',
            'verify=verify:main',
            'download=download:main',
            'latest=latest:main',
        ],
    },
)
