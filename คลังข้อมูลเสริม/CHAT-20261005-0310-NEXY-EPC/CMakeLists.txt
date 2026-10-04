cmake_minimum_required(VERSION 3.20)
project(nexy_epc LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

add_library(nexy_epc STATIC
  src/q64.cpp
  src/epc.cpp
  src/vote_ledger.cpp
)
target_include_directories(nexy_epc PUBLIC include)
target_compile_options(nexy_epc PRIVATE -Wall -Wextra -Wconversion -Wsign-conversion -Wshadow -Werror)

add_executable(epc_tests tests/test_epc.cpp)
target_link_libraries(epc_tests PRIVATE nexy_epc)
target_compile_options(epc_tests PRIVATE -Wall -Wextra -Wconversion -Wsign-conversion -Wshadow -Werror)

add_executable(epc_property_tests tests/property_epc.cpp)
target_link_libraries(epc_property_tests PRIVATE nexy_epc)
target_compile_options(epc_property_tests PRIVATE -Wall -Wextra -Wconversion -Wsign-conversion -Wshadow -Werror)

add_executable(epc_example examples/example.cpp)
target_link_libraries(epc_example PRIVATE nexy_epc)

enable_testing()
add_test(NAME epc_unit COMMAND epc_tests)
add_test(NAME epc_property COMMAND epc_property_tests)

add_executable(epc_generate_self_vote examples/generate_self_vote.cpp)
target_link_libraries(epc_generate_self_vote PRIVATE nexy_epc)
target_compile_options(epc_generate_self_vote PRIVATE -Wall -Wextra -Wconversion -Wsign-conversion -Wshadow -Werror)
