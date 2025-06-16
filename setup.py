from setuptools import setup, find_packages

setup(
    name='textcleaner',
    version='0.1.0',
    author='Rinat',
    author_email='your@email.com',
    description='Библиотека для очистки текста от мусора, HTML, эмодзи и стоп-слов',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/textcleaner',
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
