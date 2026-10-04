cmake_minimum_required(VERSION 3.20)
project(nexy_cfpc20 VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(CFPC_ENABLE_SANITIZERS "Enable ASan/UBSan" OFF)

add_library(nexy_cfpc STATIC
  src/q64.cpp
  src/sha256.cpp
  src/cfpc.cpp
)
target_include_directories(nexy_cfpc PUBLIC include)
target_compile_options(nexy_cfpc PRIVATE -Wall -Wextra -Wconversion -Wsign-conversion -Werror)

if(CFPC_ENABLE_SANITIZERS AND CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  target_compile_options(nexy_cfpc PRIVATE -fsanitize=address,undefined -fno-omit-frame-pointer)
  target_link_options(nexy_cfpc PRIVATE -fsanitize=address,undefined)
endif()

add_executable(cfpc_tests tests/test_cfpc.cpp)
target_link_libraries(cfpc_tests PRIVATE nexy_cfpc)
target_compile_options(cfpc_tests PRIVATE -Wall -Wextra -Wconversion -Wsign-conversion -Werror)
if(CFPC_ENABLE_SANITIZERS AND CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  target_compile_options(cfpc_tests PRIVATE -fsanitize=address,undefined -fno-omit-frame-pointer)
  target_link_options(cfpc_tests PRIVATE -fsanitize=address,undefined)
endif()

add_executable(cfpc_example examples/integration_example.cpp)
target_link_libraries(cfpc_example PRIVATE nexy_cfpc)
target_compile_options(cfpc_example PRIVATE -Wall -Wextra -Wconversion -Wsign-conversion -Werror)
if(CFPC_ENABLE_SANITIZERS AND CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  target_compile_options(cfpc_example PRIVATE -fsanitize=address,undefined -fno-omit-frame-pointer)
  target_link_options(cfpc_example PRIVATE -fsanitize=address,undefined)
endif()

include(CTest)
if(BUILD_TESTING)
  add_test(NAME cfpc_tests COMMAND cfpc_tests)
endif()
