cmake_minimum_required(VERSION 2.8.11)
project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(libzmq INTERFACE IMPORTED)
set_property(TARGET libzmq PROPERTY INTERFACE_COMPILE_OPTIONS ${CONAN_DEFINES})
set_property(TARGET libzmq PROPERTY INTERFACE_LINK_LIBRARIES ${CONAN_LIBS})
set_property(TARGET libzmq PROPERTY INTERFACE_INCLUDE_DIRECTORIES ${CONAN_INCLUDE_DIRS})

add_library(libzmq-static INTERFACE IMPORTED)
set_property(TARGET libzmq-static PROPERTY INTERFACE_COMPILE_OPTIONS ${CONAN_DEFINES})
set_property(TARGET libzmq-static PROPERTY INTERFACE_LINK_LIBRARIES ${CONAN_LIBS})
set_property(TARGET libzmq-static PROPERTY INTERFACE_INCLUDE_DIRECTORIES ${CONAN_INCLUDE_DIRS})

add_subdirectory("source_subfolder")
