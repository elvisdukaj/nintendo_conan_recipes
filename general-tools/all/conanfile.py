import os
from conan import ConanFile
from conan.tools.files import copy
from conan.tools.files import get, export_conandata_patches, apply_conandata_patches, copy
from conan.tools.gnu import Autotools
from conan.tools.layout import basic_layout


required_conan_version = ">=2"

class GeneralToolsConan(ConanFile):
    name = "general-tools"
    description = "Convert binary files to GCC assembly modules"
    url = "https://github.com/devkitPro/general-tools"
    homepage = "https://github.com/devkitPro/general-tools"
    # topics = ()
    settings = "os", "arch", "compiler", "build_type"
    license = "GPL-3"

    generators = "AutotoolsToolchain", "AutotoolsDeps"

    def build_requirements(self):
        self.tool_requires("pkgconf/2.2.0")
        self.tool_requires("automake/1.16.5")
        self.tool_requires("libtool/2.4.7")

    def layout(self):
        basic_layout(self)

    def export_sources(self):
        export_conandata_patches(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        apply_conandata_patches(self)
        at = Autotools(self)
        at.autoreconf()
        at.configure()
        at.make()

    def package(self):
        at = Autotools(self)
        at.install()
        copy(self, pattern="LICENSE", src=self.export_sources_folder, dst=self.package_folder) 

    def package_id(self):
        del self.info.settings.build_type
        del self.info.settings.compiler

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.buildenv_info.append_path("PATH", os.path.join(self.package_folder, "bin"))
