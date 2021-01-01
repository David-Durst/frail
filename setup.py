from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='frail',
    version='0.0.2',
    url='https://github.com/David-Durst/frail',
    license='MIT',
    maintainer='David Durst',
    maintainer_email='davidbdurst@gmail.com',
    description='Create and prove equivalence of affine indexing hardware using recurrence relations encoded in scans',
    packages=[
        "frail",
    ],
    install_requires=[
        'pysmt',
        'fault'
    ],
    python_requires='>=3.8',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
