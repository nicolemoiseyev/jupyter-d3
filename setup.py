from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
  name='jupyter_d3',
  version='0.0.2',
  url='https://github.com/nicolemoiseyev/jupyter-d3/',
  author='Nicole Moiseyev',
  author_email='nicole.moiseyev@duke.edu',
  long_description=open('README.md', 'r').read(),
  license='MIT',
  install_requires=list(map(str.strip, open('requirements.txt', 'r').readlines())),
  packages=find_packages(),
  include_package_data=True,
)
