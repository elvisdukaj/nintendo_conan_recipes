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
            self.run("bin2s -h")
            # All the tools below are not supporting a -h or -v version to test. Testing the output is enough for now
            self.run("bmp2bin", ignore_errors=True)
            self.run("generate_compile_commands", ignore_errors=True)  # I don't understand this yet
            self.run("padbin", ignore_errors=True)
            self.run("raw2c", ignore_errors=True)

