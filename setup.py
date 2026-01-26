from setuptools import setup, find_packages
from typing import List
hyphen_e_dot = '-e .'
def get_requirements(file_path) -> List[str]:
    with open(file_path, 'r') as file:
        requirements = file.readlines()
        requirements= [req.strip() for req in requirements if req.strip()]
        
        if hyphen_e_dot in requirements:
            requirements.remove(hyphen_e_dot) #to remove the -e . from the list
    return requirements
setup(
    name="ML-STUDENTPERFORMANCEPROJECT",
    version="0.0.1",
    author="Symniya",
    author_email="symniya09@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)