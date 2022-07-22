project(clang-tidy-wheel)
cmake_minimum_required(VERSION 3.16)

# Include the "single source of truth" for the clang-tidy version
include(clang-tidy_version.cmake)
string(REPLACE "-" "" CLANG_TIDY_VERSION_SHORT "${CLANG_TIDY_VERSION}")

# Define a build rule clang-tidy
set(LLVM_DOWNLOAD_URL "https://github.com/llvm/llvm-project/releases/download/llvmorg-${CLANG_TIDY_VERSION}/llvm-project-${CLANG_TIDY_VERSION_SHORT}.src.tar.xz")
include(ExternalProject)
ExternalProject_add(build-clang-tidy
  URL "${LLVM_DOWNLOAD_URL}"
  SOURCE_SUBDIR llvm
  SOURCE_DIR ${CMAKE_BINARY_DIR}/llvm-project
  BINARY_DIR ${CMAKE_BINARY_DIR}/llvm
  UPDATE_COMMAND ""
  INSTALL_COMMAND ""
  USES_TERMINAL_DOWNLOAD 1
  USES_TERMINAL_CONFIGURE 1
  USES_TERMINAL_BUILD 1
  CMAKE_ARGS -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DLLVM_ENABLE_PROJECTS=clang$<SEMICOLON>clang-tools-extra
  BUILD_COMMAND ${CMAKE_COMMAND} --build . --target clang-tidy
)
set(clang-tidy-executable ${CMAKE_BINARY_DIR}/llvm/bin/clang-tidy${CMAKE_EXECUTABLE_SUFFIX})

# Reduce the size of the executable by executing strip if it is present on the system
find_program(STRIP_EXECUTABLE strip)
if(STRIP_EXECUTABLE)
  add_custom_target(
    strip-clang-tidy
    ALL
    COMMAND ${STRIP_EXECUTABLE} ${clang-tidy-executable}
    COMMENT "Stripping clang-tidy executable for size reduction"
  )
  add_dependencies(strip-clang-tidy build-clang-tidy)
endif()

# Define an installation rule that copies the executable to our Python package
install(
  PROGRAMS
    ${clang-tidy-executable}
  DESTINATION clang_tidy/data/bin
)

install(
  DIRECTORY
    ${CMAKE_BINARY_DIR}/llvm/lib/clang/${CLANG_TIDY_VERSION}/include
  DESTINATION clang_tidy/data/lib/clang/${CLANG_TIDY_VERSION}
)
