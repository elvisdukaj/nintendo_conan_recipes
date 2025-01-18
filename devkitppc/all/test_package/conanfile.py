from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.scm import Version


class TestPackgeConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeToolchain", "VirtualBuildEnv"
    test_type = "explicit"

    def build_requirements(self):
        self.tool_requires(self.tested_reference_str)

    def layout(self):
        cmake_layout(self)

    def build(self):
        if self.settings.os == "NintendoWii":
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

    def test(self):
        self.run("powerpc-eabi-g++ --version", env="conanbuild")
