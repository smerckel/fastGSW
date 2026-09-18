import os
import sys

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext as _build_ext

CSRC = os.path.join("src", "fast_gsw", "_csrc")
SOURCES = [
    os.path.join(CSRC, "gsw_oceanographic_toolbox.c"),
    os.path.join(CSRC, "gsw_saar.c"),
    os.path.join(CSRC, "gsw_vector.c"),
]


class ctypes_build_ext(_build_ext):
    """Build a plain shared library (no CPython C-API) for loading via
    ctypes.CDLL, named like a normal shared object rather than an
    importable CPython extension module.
    """

    def get_export_symbols(self, ext):
        return []

    def get_ext_filename(self, ext_name):
        parts = ext_name.split(".")
        if sys.platform.startswith("linux"):
            return os.path.join(*parts) + ".so"
        elif sys.platform == "darwin":
            return os.path.join(*parts) + ".dylib"
        elif sys.platform == "win32":
            return os.path.join(*parts) + ".dll"
        return super().get_ext_filename(ext_name)

    def build_extension(self, ext):
        objects = self.compiler.compile(
            ext.sources,
            output_dir=self.build_temp,
            include_dirs=ext.include_dirs,
            extra_postargs=ext.extra_compile_args,
        )
        ext_path = self.get_ext_fullpath(ext.name)
        os.makedirs(os.path.dirname(ext_path), exist_ok=True)
        self.compiler.link_shared_object(
            objects,
            ext_path,
            libraries=ext.libraries,
            extra_postargs=ext.extra_link_args,
        )


libgsw_vector = Extension(
    "fast_gsw.libgsw_vector",
    sources=SOURCES,
    include_dirs=[CSRC],
    libraries=["m"],
    extra_compile_args=["-O3", "-fPIC"],
)

setup(
    ext_modules=[libgsw_vector],
    cmdclass={"build_ext": ctypes_build_ext},
)
