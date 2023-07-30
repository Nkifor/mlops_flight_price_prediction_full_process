from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(filename:str)->List[str]:
    """
    Get requirements from file.
    """
    requirements = []
    with open(filename) as file_obj:
        requirements=file_obj.readlines()
        requirements = [x.replace("\n", "") for x in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements


setup(
    name='mlops heart disease indicators full process',
    version='0.1',
    author='Krzysztof',
    author_email='stasiek3000@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
)