project(test_package)
cmake_minimum_required(VERSION 3.1)


include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

file(GLOB SOURCE_FILES *.cpp)

add_executable(${PROJECT_NAME} ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})
