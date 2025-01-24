import os
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get, rm, export_conandata_patches, apply_conandata_patches 
from conan.tools.cmake import CMakeDeps, CMakeToolchain, CMake
from conan.tools.layout import basic_layout


required_conan_version = ">=2"

class OpenGXConan(ConanFile):
    name = "opengx"
    description = "OpenGL-like wrapper for Nintendo Wii/GameCube"
    url = "https://github.com/devkitPro/opengx"
    homepage = "https://github.com/devkitPro/opengx"
    license = "MIT"
    package_type = "static-library"
    topics = ("nintendo", "Wii", "GameCube", "opengl")
    settings = "os", "arch", "compiler", "build_type"

    def requirements(self):
        self.requires("libogc/2.10.0")

    def validate(self):
        valid_os = ["NintendoWii"]
        if str(self.settings.os) not in valid_os:
            raise ConanInvalidConfiguration(f"{self.name} {self.version} is only supported for the following operating systems: {valid_os}")

    def export_sources(self):
        export_conandata_patches(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def layout(self):
        basic_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        rm(self, pattern="*", folder=os.path.join(self.package_folder, "lib", "cmake"))
        rm(self, pattern="*", folder=os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        supported_os = ["NintendoWii", "NintendoGameCube"]
        if self.settings.os not in supported_os:
            self.output.warning(f"{self.settings.os} not supported. Supported os are {supported_os}")

        self.cpp_info.lib = ["opengx"]
        self.cpp_info.set_property("cmake_file_name", "OpenGL")
        self.cpp_info.set_property("cmake_target_name", "OpenGL::GL")
        self.cpp_info.requires = ["libogc::ogc"]

        self.cpp_info.set_property("pkg_config_name", "opengl")



