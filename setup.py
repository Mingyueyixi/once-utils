import os.path

from setuptools import setup, find_packages


def readme_md():
    readme_md_path = os.path.join('README.md')
    ret = ''
    with open(readme_md_path) as f:
        ret = f.read()
    return ret


setup(
    name="once-utils",
    version="0.0.3",
    keywords=["pip", "once-utils"],
    description="Simplest utils.",
    long_description=readme_md(),
    long_description_content_type='text/markdown',
    license="MIT Licence",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers'],

    url="https://github.com/Mingyueyixi/once-utils",
    author="Lu",
    author_email="Mingyueyixi@hotmail.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)
