from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.layout import basic_layout


class TestPackgeConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeToolchain", "VirtualBuildEnv"
    test_type = "explicit"

    generators = "CMakeToolchain", "CMakeDeps"

    def layout(self):
        basic_layout(self)

    def requirements(self):
        self.requires(self.tested_reference_str)

    def test(self):
        if can_run(self):
            self.run("flock --version")
