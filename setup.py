from setuptools import setup, find_packages

setup(
    name='aethra',
    version='0.1.4',
    author='Aethra',
    author_email='achref.benammar@ieee.org',
    description='A Python client library for Aethra API',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/AethraData/aethra.git",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'pydantic>=1.8.2',
        'python-dotenv>=0.15.0',
        'networkx==3.4.2',
        'numpy==2.2.1'
    ],
    license='Apache License 2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
