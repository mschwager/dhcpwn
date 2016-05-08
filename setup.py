from setuptools import setup

import os.path

requirements_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')

with open(requirements_filename) as fd:
    install_requires = [i.strip() for i in fd.readlines()]

setup(
    name='dhcpwn',
    version='1.0',
    description='All your IPs are belong to us.',
    url='https://github.com/mschwager/dhcpwn',
    py_modules=['dhcpwn'],
    license='GPLv3',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'dhcpwn = dhcpwn:main',
        ],
    },
)
