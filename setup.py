from setuptools import setup, find_packages

setup(
    name='kangaroo-tools',
    version='0.2.0',
    author='Rinat',
    author_email='rinat.islamov.04@gmail.com',
    description='Библиотека для очистки текста от мусора, HTML, эмодзи и стоп-слов',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Seraphim04174/kangaroo-tools',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'nltk>=3.9.1',
        'emoji>=2.14.1',
    ],
    python_requires='>=3.7',
)
