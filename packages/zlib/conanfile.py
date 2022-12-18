from conans import ConanFile
from conans.tools import download, unzip
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.13esri1"
    settings = "os", "compiler", "build_type", "arch"

    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    exports_sources = "include/*"
    no_copy_source = True

    def source(self):
        download("https://zlib.net/zlib-1.2.13.tar.gz", "zlib-1.2.13.tar.gz")
        unzip("zlib-1.2.13.tar.gz", destination='.', strip_root=True)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self, generator='Ninja')
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ['libz.a']
