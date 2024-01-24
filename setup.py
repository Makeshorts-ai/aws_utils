from setuptools import setup, find_packages

setup(
    name='aws_utils',   # The name of your package
    version='0.1.0',        # The version of your package
    packages=find_packages(),  # Automatically discover and include all packages in your project

    install_requires=[
        'requests'
    ],
)
