"""Install CGS_parcels and dependencies."""

from setuptools import setup,find_packages

def get_install_requires():
    install_requires=[
        'parcels',
        'ipywidgets',
        'cachetools >= 1.0.0',
        'cgen',
        'coverage',
        'flake8 >= 2.1.0',
        'jupyter',
        'ffmpeg-python',
        'matplotlib >= 2.0.2',
        'netcdf4 >= 1.1.9',
        'numpy >= 1.9.1',
        'progressbar2',
        'py >= 1.4.27',
        'pymbolic',
        'python-dateutil',
        'scipy >= 0.16.0',
        'six >= 1.10.0',
        'xarray >= 0.5.1',
        'nbval',
        'ast',
        'requests']
    return install_requires

setup(name='CGS_parcels',
      version='1.0',
      description='Framework for Contextual Geometric Structure using Parcels\
        package for flow field simulation.',
      author='jimboH',
      author_email='jimbokururu27@gmail.com',
      license='MIT',
      packages=find_packages(),
      url='https://github.com/Orthogonal-Research-Lab/CGS',
      zip_safe=False,
      python_requires='>=2.7, <3',
      dependency_links=['git+https://github.com/OceanParcels/parcels.git@master#egg=parcels-1.0'],
      tests_require=['pytest >= 2.7.0'],
      install_requires=get_install_requires()
      )

