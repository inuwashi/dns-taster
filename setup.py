from setuptools import setup

setup(
    name='dns_taster',
    version='0.1',
    py_modules=['dns_taster'],
    install_requires=[
        'Click',
        'dnspython',
        'validators',
    ],
    entry_points='''
        [console_scripts]
        dns_taster=dns_taster:taste
    ''',
)
