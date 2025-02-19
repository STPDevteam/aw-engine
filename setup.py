from setuptools import setup, find_packages, Extension
import pybind11

persona_dependency_module = Extension('aw_engine_cpp',
                                      sources=['csrc/persona_dependency.cpp'],
                                      include_dirs=[pybind11.get_include(), '/usr/include/hiredis'],
                                      library_dirs=['/usr/lib/x86_64-linux-gnu'],
                                      libraries=['hiredis'],
                                      language='c++')

setup(name='aw_engine',
      version='0.1',
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      ext_modules=[persona_dependency_module],
      install_requires=['redis', 'pybind11'],
      python_requires='>=3.6',
      author='Autonomous Worlds Engine from AWE Network')
