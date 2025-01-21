import os
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get, copy, patch
from conan.tools.build import build_jobs
from conan.tools.layout import basic_layout
from conans.model.conan_file import Path


required_conan_version = ">=2"

class LibogcConan(ConanFile):
    name = "libogc"
    description = "C Library for Wii and Gamecube homebrew"
    url = "https://github.com/devkitPro/libogc"
    homepage = "https://github.com/devkitPro/libogc"
    license = "MIT"
    topics = ("gcc", "nintendo", "wii")
    settings = "os", "arch", "compiler", "build_type"

    options = { "with_extra_libs": [True, False] }
    default_options = { "with_extra_libs": False }

    @property
    def _cmake_install_base_path(self):
        return os.path.join("lib", "cmake", "libogc")

    def validate(self):
        valid_os = ["NintendoWii"]
        if str(self.settings.os) not in valid_os:
            raise ConanInvalidConfiguration(f"{self.name} {self.version} is only supported for the following operating systems: {valid_os}")

    def export_sources(self):
        copy(self,
             pattern="*.patch", 
             src=self.recipe_folder,
             dst=self.export_sources_folder
             )
        copy(self,
             pattern="*.cmake",
             src=self.recipe_folder,
             dst=self.export_sources_folder
             )

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build_requirements(self):
        self.tool_requires("gamecube-tools/1.0.6")
        self.tool_requires("general-tools/1.4.4")
        self.tool_requires("flock/0.4.0")

    def layout(self):
        basic_layout(self)

    def _apply_patch_base(self, patch_descriptions: list[str], patch_path: Path):
        patch_files = sorted(patch_path.glob("*.patch"))
        for file, description in zip(patch_files, patch_descriptions):
            patch(
                self, 
                patch_file=file,
                patch_string=description
            )

    def _apply_patches(self):
        if self.settings.os == "NintendoWii":
            patch_descriptions = [     
                "Exclude the Cube platform for the building",
                "Allow custom installation path not related to DEVKITPRO environment",
                "Avoid installing libs in lib/wii"
            ]
            patch_path = Path(self.export_sources_folder, "patches", self.version, "wii")
            self._apply_patch_base(patch_descriptions, patch_path)
        else:
            patch_descriptions = [     
                "Exclude the Cube platform for the building",
                "Allow custom installation path not related to DEVKITPRO environment",
                "Avoid installing libs in lib/wii"
            ]
            patch_path = Path(self.export_sources_folder, "patches", self.version, "wii")
            self._apply_patch_base(patch_descriptions, patch_path)

    def build(self):
        self._apply_patches()

        # No generate is required as the Makefile utilities are present in the devkitpro toolchain file. Just calling make is enough
        # self.run(f"make SHELL='bash -c' -j{build_jobs(self)}", cwd=self.source_folder, env="conanbuild")
        self.run(f"make -j{build_jobs(self)}", cwd=self.source_folder, env="conanbuild")

    def package(self):
        self.run(f"make install DESTDIR={self.package_folder}", cwd=self.source_folder, env="conanbuild")
        cmake_config_folder = os.path.join(self.package_folder, self._cmake_install_base_path)
        copy(self,
             pattern="*.cmake",
             src=self.source_folder,
             dst=cmake_config_folder
             )

    def package_info(self):
        self.cpp_info.defines = ["GEKKO"]

        wii_ogc_libs = ["wiiuse", "bte", "ogc"]
        # TODO: enable GameCube? We need to apply different set of patches for this
        # game_cube_libs = ["bba", "ogc"]
        extra_libs = [
            "aesnd",
            "asnd",
            "db",
            "iso9660",
            "mad",
            "modplay",
            "tinysmb",
        ]
        wii_extra_libs = ["di", "wiikeyboard"]

        # TODO: enable GameCube? We need to apply different set of patches for this
        # supported_os = ["NintendoWii", "NintendoGameCube"]
        supported_os = ["NintendoWii"]
        if self.settings.os not in supported_os:
            self.output.warning(f"{self.settings.os} not supported. Supported os are {supported_os}")

        if self.settings.os == "NintendoWii":
            self.cpp_info.libs = wii_ogc_libs
            if self.options.with_extra_libs is True:
                self.cpp_info.libs.extend(extra_libs)
                self.cpp_info.libs.extend(wii_extra_libs)
            
        # TODO: add support for GameCube: adding 
        # if self.settings.os == "NintendoGameCube":
            # self.cpp_info.libdirs = ["lib/cube"]
            # self.cpp_info.libs = game_cube_libs
            # if self.options.with_extra_libs is True:
                # self.cpp_info.libs.extend(extra_libs)

        self.cpp_info.system_libs = ["m"]

        # extra cmake modules to be included when using find_package
        build_modules = [
            os.path.join(self._cmake_install_base_path, "gamecube-tools.cmake"),
            os.path.join(self._cmake_install_base_path, "general-tools.cmake"),
            os.path.join(self._cmake_install_base_path, "flock-tools.cmake"),
        ]
        self.cpp_info.set_property("cmake_build_modules", build_modules)





