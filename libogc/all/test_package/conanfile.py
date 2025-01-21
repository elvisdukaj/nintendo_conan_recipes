from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import can_run
from conan.tools.cmake import CMake, cmake_layout, CMakeDeps, CMakeToolchain


class TestPackgeConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    test_type = "explicit"

    def build_requirements(self):
        self.tool_requires("devkitppc/r46.1")
        self.tool_requires("gamecube-tools/1.0.6")
        self.tool_requires("general-tools/1.4.4")
        self.tool_requires("flock/0.4.0")
        
    def requirements(self):
        self.requires(self.tested_reference_str)


    def validate(self):
        if self.settings.os not in ["NintendoWii"]:
            raise ConanInvalidConfiguration(f"{str(self.settings.os)} is not supported! Only Nintendo Wii is supported")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.cache_variables["CMAKE_VERBOSE_MAKEFILE"] = True
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        # test all the tools are in the path
        self.run("flock --version")
        self.run("bin2s -h")
        # All the tools below are not supporting a -h or -v version to test. Testing the output is enough for now
        self.run("bmp2bin", ignore_errors=True)
        self.run("generate_compile_commands", ignore_errors=True)  # I don't understand this yet
        self.run("padbin", ignore_errors=True)
        self.run("raw2c", ignore_errors=True)

        if can_run(self):
            self.run("./test_package", env="conanrun")
