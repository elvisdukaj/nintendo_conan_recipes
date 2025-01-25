from conan import ConanFile
from conan.tools.layout import basic_layout


class TestPackgeConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    test_type = "explicit"

    def layout(self):
        basic_layout(self)

    def requirements(self):
        self.requires(self.tested_reference_str)

    def test(self):
        self.run("flock --version")
