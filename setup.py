from numpy.lib.utils import get_include
from setuptools import setup
from Cython.Build import cythonize

setup(
    name="RutinaVicsek",
    ext_modules=cythonize("RutinaVicsek.pyx", annotate=True),
    include_dirs=[get_include()],
    zip_safe=False
)
