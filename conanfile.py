from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
import os
import stat
import fnmatch

class CdparanoiaConan(ConanFile):
    name = "cdparanoia"
    version = "10.2"
    description = "An audio CD reading utility which includes extra data verification features"
    url = "https://github.com/conanos/cdparanoia"
    homepage = "https://www.xiph.org/paranoia/"
    license = "LGPL v2.1+"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    source_subfolder = "source_subfolder"

    def source(self):
        url_ = 'http://downloads.xiph.org/releases/cdparanoia/{name}-III-{version}.src.tgz'
        tools.get(url_.format(name=self.name, version=self.version))
        os.rename("%s-III-%s"%(self.name, self.version), self.source_subfolder)

    def build(self):
        with tools.chdir(self.source_subfolder):
            self.run("autoreconf -f -i")

            autotools = AutoToolsBuildEnvironment(self)
            autotools.fpic = True
            _args = ['--prefix=%s/builddir'%(os.getcwd()), '--libdir=%s/builddir/lib'%(os.getcwd()),
                     '--disable-maintainer-mode', '--disable-silent-rules']

            autotools.configure(args=_args)
            autotools.make(args=["-j2"])
            autotools.install()

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("*", src="%s/builddir"%(os.getcwd()))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

