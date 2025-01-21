from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.layout import basic_layout
from conan.tools.scm import Version
from conan.tools.build import can_run


class TestPackgeConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeToolchain", "VirtualBuildEnv"
    test_type = "explicit"

    generators = "CMakeToolchain", "CMakeDeps"

    def build_requirements(self):
        self.tool_requires(self.tested_reference_str)

    def layout(self):
        cmake_layout(self)

    def build(self):
        valid_os = ["NintendtoWii", "NintendoGameCube"]
        if self.settings.get_safe("os") in valid_os:
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

    def test(self):
        if can_run(self):
            self.run("gcdsptool -h")
            self.run("elf2dol -h")
            self.run("gxtexconv -h")

