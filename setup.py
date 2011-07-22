from setuptools import setup, find_packages


setup(
    name="magnatune",
    version="0.2",
    packages=find_packages(),

    author="Georges Dubus",
    author_email="georges.dubus@compiletoi.net",
    description="Command line utility and lib to interact with the music "
                "website magnatune",
    long_description=open('README.rst', 'rt').read(),
    url="https://github.com/madjar/python-magnatune",
    license="GPLv3",
    keywords="magnatune music stream",

    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia",
        ],


    install_requires=['lxml'],
    tests_require=['nose', 'Mock'],
    entry_points={'console_scripts': ['magnatune = magnatune.main:main']}
)
