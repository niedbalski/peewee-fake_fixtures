from setuptools import setup, find_packages

dependencies = [ "peewee", "fake-factory" ]

setup(
    name="peewee-fake-fixtures",
    version="0.2",
    packages=find_packages(),
    install_requires=dependencies,
    author="Jorge Niedbalski R.",
    author_email="jnr@pyrosome.org",
    description="A Python based fixture generator for peewee databases",
    keywords="fixture generator fake fake-factory peewee fixtures",
    license="BSD",

    classifiers=['Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',
                'Operating System :: Unix ']
)
