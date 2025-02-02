from setuptools import setup, find_packages

setup(
    name='Aiklyra',
    version='1.0.2',
    author='Aiklyra',
    author_email='achref.benammar@ieee.org',
    description='A Python client library for Aiklyra API',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/aiklyra/aiklyra.git",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'pydantic>=1.8.2',
        'python-dotenv>=0.15.0',
        'networkx==3.4.2',
        'numpy<2.0',
        'matplotlib<=3.10.0',
        'pyvis==0.3.2'
    ],
    license='Apache License 2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
