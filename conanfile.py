from conans import ConanFile, CMake, tools
import os


class ZmqPPConan(ConanFile):
    name = "zmqpp"
    version = "4.2.0"
    description = "0mq 'highlevel' C++ bindings"
    url = "https://github.com/bincrafters/conan-zmqpp"
    homepage = "https://github.com/zeromq/zmqpp"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MPL 2.0"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, 'fPIC': True}

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def requirements(self):
        self.requires.add('zmq/4.2.2@bincrafters/stable')

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/zeromq/zmqpp"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)
        tools.replace_in_file(os.path.join(self._source_subfolder, 'CMakeLists.txt'),
                              'target_link_libraries(zmqpp ws2_32)',
                              'if(ZMQPP_BUILD_SHARED)\n'
                              'target_link_libraries(zmqpp ws2_32 iphlpapi)\n'
                              'endif()')
        tools.replace_in_file(os.path.join(self._source_subfolder, 'CMakeLists.txt'),
                              'generate_export_header(zmqpp)',
                              'if(ZMQPP_BUILD_SHARED)\n'
                              'generate_export_header(zmqpp)\n'
                              'else()\n'
                              'generate_export_header(zmqpp-static BASE_NAME zmqpp)\n'
                              'endif()')
        tools.replace_in_file(os.path.join(self._source_subfolder, 'src', 'zmqpp', 'zap_request.cpp'),
                              '#include', '#include <iterator>\n#include')
        tools.replace_in_file(os.path.join(self._source_subfolder, 'src', 'zmqpp', 'socket.cpp'),
                              'std::min', '(std::min<size_t>)')

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['ZMQPP_BUILD_STATIC'] = not self.options.shared
        cmake.definitions['ZMQPP_BUILD_SHARED'] = self.options.shared
        cmake.definitions['ZMQPP_BUILD_EXAMPLES'] = False
        cmake.definitions['ZMQPP_BUILD_CLIENT'] = False
        cmake.definitions['ZMQPP_BUILD_TESTS'] = False
        cmake.definitions['ZMQPP_LIBZMQ_CMAKE'] = True
        cmake.definitions['ZMQPP_LIBZMQ_NAME_STATIC'] = self.deps_cpp_info['zmq'].libs[0]
        cmake.definitions['ZMQPP_LIBZMQ_NAME_SHARED'] = self.deps_cpp_info['zmq'].libs[0]
        cmake.definitions['ZEROMQ_LIB_DIR'] = self.deps_cpp_info['zmq'].lib_paths[0]
        cmake.definitions['ZEROMQ_INCLUDE_DIR'] = self.deps_cpp_info['zmq'].include_paths[0]
        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ['zmqpp' if self.options.shared else 'zmqpp-static']
