from setuptools import setup, find_packages

setup(
    name='ConvoLens',
    version='0.1.0',
    author='Aethra Data',
    author_email='achref.benammar@ieee.org',
    description='A Python client library for ConvoLens API',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AethraData/ConvoLens.git',  # Update with your repository URL
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'pydantic>=2.0.0',
        'python-dotenv>=0.15.0'
    ],
    license='Apache License 2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
