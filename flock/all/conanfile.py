from conan import ConanFile
from conan.tools.files import get, export_conandata_patches, apply_conandata_patches, copy
from conan.tools.gnu import Autotools
from conan.tools.layout import basic_layout


required_conan_version = ">=2"

class FlockConan(ConanFile):
    name = "flock"
    description = "flock(1) locks files"
    url = "https://github.com/discoteq/flock"
    homepage = "https://github.com/discoteq/flock"
    topics = ("portable", "boring")
    settings = "os", "arch", "compiler", "build_type"
    license = "ISC"
    package_type = "application"
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
        copy(self, pattern="LICENSE.md", src=self.export_sources_folder, dst=self.package_folder) 

    def package_id(self):
        del self.info.settings.build_type
        del self.info.settings.compiler

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
