from setuptools import setup

import os.path

requirements_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')

with open(requirements_filename) as fd:
    install_requires = [i.strip() for i in fd.readlines()]

requirements_dev_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'requirements-dev.txt')

with open(requirements_filename) as fd:
    tests_require = [i.strip() for i in fd.readlines()]

setup(
    name='dhcpwn',
    version='1.0.3',
    description='All your IPs are belong to us.',
    url='https://github.com/mschwager/dhcpwn',
    py_modules=['dhcpwn'],
    license='GPLv3',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Security',
    ],
    install_requires=install_requires,
    tests_require=tests_require,
    entry_points={
        'console_scripts': [
            'dhcpwn = dhcpwn:main',
        ],
    },
)
