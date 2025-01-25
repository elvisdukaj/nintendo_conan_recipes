from conan import ConanFile
from conan.tools.layout import basic_layout


class TestPackgeConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    test_type = "explicit"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def layout(self):
        basic_layout(self)

    def test(self):
        self.run("gcdsptool -h")
        self.run("elf2dol -h", ignore_errors=True)
        self.run("gxtexconv -h")

