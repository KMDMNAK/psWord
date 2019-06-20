from setuptools import setup,find_packages
"""
setup(
    name="scraping_tools",
<<<<<<< HEAD
    version="1.2.0",
=======
    version="1.0.3",
>>>>>>> origin/master
    install_requires=["requests"],
    packages=find_packages()
)"""

setup(
    name="psWord",
    version="1.0.0",
    install_requires=["gensim","matplotlib","networkx","MeCab","googletrans"],
    packages=find_packages()
)

