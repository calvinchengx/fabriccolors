from distutils.core import setup

setup(
    name='FabricColors',
    version='0.1dev',
    packages=['fabric-colors', ],
    license='LICENSE',
    description='The easiest way to set-up your server or virtual machine using pre-defined templates for python fabric',
    long_description=open('README.md').read(),
    author='Calvin Cheng',
    author_email='calvin@calvinx.com',
    install_requires=[
        "fabric >= 1.4.1",
    ],
    entry_points={
        'console_scripts': [
            'fabc = fabriccolors.main:main',
        ]
    }
)
