from setuptools import setup, find_packages

setup(
    name='kangaroo-tools',
    version='0.1.1',
    author='Rinat',
    author_email='rinat.islamov.04@gmail.com',
    description='Библиотека для очистки текста от мусора, HTML, эмодзи и стоп-слов',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Seraphim04174/kangaroo-tools.git',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        'nltk',
        'emoji',
        'beautifulsoup4'
    ],
    python_requires='>=3.7',
)
