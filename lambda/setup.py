from setuptools import setup, find_packages

setup(
    name="wpwithinpy",
    version="0.1",
    packages=['wpwithinpy'],
    install_requires=[
        'json-cfg',
        'thrift'
    ],
    include_package_data=True
)
