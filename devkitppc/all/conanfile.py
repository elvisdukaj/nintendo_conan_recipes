import os
from pathlib import Path
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get, export_conandata_patches, apply_conandata_patches, copy
from conan.tools.layout import basic_layout
from conan.tools.env import VirtualBuildEnv


required_conan_version = ">=2"


class DevKitProConan(ConanFile):
    name = "devkitppc"
    description = "Toolchain to target the Nintendo Wii and GameCube console"
    url = "https://github.com/devkitpro"
    homepage = "https://github.com/devkitpro"
    license = ""
    package_type = "application"
    topics = ("gcc", "nintendo", "wii")
    settings = "os"

    @property
    def _settings_target(self):
        return getattr(self, "settings_target", None)

    @property
    def _settings_target_compiler(self):
        if self._settings_target:
            return self._settings_target.get_safe("compiler")

    @property
    def _settings_target_os(self):
        if self._settings_target:
            return self._settings_target.get_safe("os")

    def requirements(self):
        self.requires("make/4.4.1")
        self.requires("bison/3.8.2")
        self.requires("flex/2.6.4")
        self.requires("gettext/0.22.5")
        self.requires("gsl/2.7.1")
        self.requires("gmp/6.3.0")
        self.requires("mpfr/4.2.0")
        self.requires("mpc/1.3.1")
        self.requires("readline/8.2")
        self.requires("libarchive/3.7.6")
        self.requires("openssl/3.3.2")
        self.requires("libtool/2.4.7")

    def validate(self):
        valid_os = ["Macos"]
        if str(self.settings.os) not in valid_os:
            raise ConanInvalidConfiguration(f"{self.name} {self.version} is not supported in {str(self.settings.os)} only supported for the following operating systems: {valid_os}")

    def export_sources(self):
        export_conandata_patches(self)
        copy(self, pattern="*.cmake", src=self.recipe_folder, dst=self.export_sources_folder)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def layout(self):
        basic_layout(self)

    def generate(self):
        be = VirtualBuildEnv(self)
        env = be.environment()
        env.define("BUILD_DKPRO_PACKAGE", "2")   # BUILD_DKPRO_PACKAGE == "2" --> devkitPPC
        env.define("BUILD_DKPRO_AUTOMATED", "1") # for non-interactive shell
        env.define("INSTALLDIR", str(self.package_folder))
        be.generate()

    def build(self):
        apply_conandata_patches(self)

    def package(self):
        self.run("./build-devkit.sh", env="conanbuild", cwd=Path(self.build_folder).parent)
        copy(self,
             pattern="*.cmake",
             src=self.export_sources_folder,
             dst=self.package_folder,
             excludes="test_package/*"
             )

    @property
    def _toolchain_bin_path(self) -> Path:
        return Path(self.package_folder, "devkitPPC", "bin")

    _toolchain_prefix: str = "powerpc-eabi"

    def _tool_path(self, tool: str) -> Path:
        return Path(self._toolchain_bin_path, f"{self._toolchain_prefix}-{tool.lower()}")

    def _tool_name_define(self, name: str) -> str:
        tool_map = {
            "gcc": "CC",
            "g++": "CXX",
        }
        return tool_map.get(name.lower(), name.upper())

    def _define_build_env_tool(self, name: str):
        self.buildenv_info.define_path(self._tool_name_define(name), str(self._tool_path(name)))

    def package_info(self):
        arch_flags: str = "-mcpu=750 -meabi -mhard-float -ffunction-sections -fdata-sections"

        if self._settings_target_compiler != "devkitppc":
            self.output.warning("Only devkitPPC toolchain is supported!")

        supported_os = ["NintendoWii"]
        # TODO: supported_os = ["NintendoWii", "NintendoGameCube"]
        if self._settings_target_os not in supported_os:
            self.output.warning(f"{self._settings_target_os} not supported. Supported os are {supported_os}")

        if self._settings_target_os == "NintendoWii":
            arch_flags = "-mrvl" + " " + arch_flags

        # TODO: Add support for GameCube: adding -mogc makes libogc to fail
        # if self._settings_target_os == "NintendoGameCube":
            # arch_flags = "-mogc" + " " + arch_flags

        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs.append(self._toolchain_bin_path)

        self.buildenv_info.define_path("DEVKITPRO", self.package_folder)
        self.buildenv_info.define_path("DEVKITPPC", os.path.join(self.package_folder, "devkitPPC"))
        
        self._define_build_env_tool("ar")
        self._define_build_env_tool("as")
        self._define_build_env_tool("gcc")
        self._define_build_env_tool("g++")
        self._define_build_env_tool("ld")
        self._define_build_env_tool("ranlib")
        self._define_build_env_tool("strip")
        self._define_build_env_tool("nm")
        self._define_build_env_tool("objcopy")
        self._define_build_env_tool("objdump")
        self._define_build_env_tool("readelf")

        compiler_executables = {
            "c": self._tool_path("gcc"),
            "cpp": self._tool_path("g++"),
            "as": self._tool_path("as"),
        }
        self.conf_info.update("tools.build:compiler_executables", compiler_executables)

        self.buildenv_info.define("CFLAGS", arch_flags)
        self.buildenv_info.define("CPPFLAGS", arch_flags)
        self.buildenv_info.define("CXXFLAGS", arch_flags)
        self.buildenv_info.define("LDFLAGS", arch_flags)

        self.conf_info.append("tools.build:cflags", arch_flags)
        self.conf_info.append("tools.build:cxxflags", arch_flags)
        self.conf_info.append("tools.build:sharedlinkerflags", arch_flags)
        self.conf_info.append("tools.build:exelinkerflags", arch_flags)

        cmake_user_toolchain = os.path.join(self.package_folder, "cmake", "Wii.cmake")
        self.conf_info.append("tools.cmake.cmaketoolchain:user_toolchain", cmake_user_toolchain)
