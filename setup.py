from setuptools import setup,find_packages

setup(
    name="psWord",
    version="1.0.2",
    install_requires=["gensim","matplotlib","networkx","mecab-python3","googletrans"],
    package_dir={'home':'','parse':"parse","network":"network","gensim":"GensimWrapper"},
    #packages=find_packages()
    packages=["home","parse","network","gensim"]
)

