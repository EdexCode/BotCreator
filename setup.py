from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Easy chatbot development with Python. Create your own chatbots with just a few lines of code.'
# Setting up
setup(
    name="botcreator",
    version=VERSION,
    author="EdexCode",
    author_email="edexcode@gmail.com",
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['random'],
    keywords=['python', 'bot', 'chatbot', 'botdeveloper', 'predefined'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
