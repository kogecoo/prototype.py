from setuptools import setup, find_packages

setup(
    name='prototype.py',
    data_files=[('', ['requirements.txt', 'README.md', '.gitignore']), ],
    version='0.1.0',
    packages=find_packages(),
    description='Append some useful methods to list/tuple/GeneratorType',
    long_description='Append some useful methods to list/tuple/GeneratorType',
    author='kogecoo',
    author_email='kogecoo+prototype@gmail.com',
    license='Apache 2.0',
    url='https://github.com/kogecoo/prototype.py',
    platforms=['any'],
    install_requires=["Python-Parallel-Collections>=1.2.0"],
    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
    ],
)
