from setuptools import setup,find_packages

setup(
    name="psWord",
    version="1.0.3",
    install_requires=["gensim","matplotlib","networkx","mecab-python3","googletrans"],
    package_dir={'home':'','parse':"psWord/parse","network":"psWord/network","gensim":"psWord/GensimWrapper"},
    packages=find_packages()
    #packages=["home","parse","network","gensim"]
)

