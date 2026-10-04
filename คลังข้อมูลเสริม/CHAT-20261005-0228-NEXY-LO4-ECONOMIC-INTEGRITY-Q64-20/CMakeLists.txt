cmake_minimum_required(VERSION 3.20)
project(nexy_lo4_q64_innovation_forge VERSION 0.1.0 LANGUAGES CXX)

option(LO4_ENABLE_SANITIZERS "Enable address/undefined sanitizers" OFF)

add_library(nexy_lo4 STATIC
    src/concepts.cpp
)
target_include_directories(nexy_lo4 PUBLIC include)
target_compile_features(nexy_lo4 PUBLIC cxx_std_20)
target_compile_options(nexy_lo4 PRIVATE -Wall -Wextra -Wshadow -Wconversion -Werror)

function(lo4_enable_sanitizers target_name)
    if(LO4_ENABLE_SANITIZERS AND CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        target_compile_options(${target_name} PRIVATE -fsanitize=address,undefined -fno-omit-frame-pointer)
        target_link_options(${target_name} PRIVATE -fsanitize=address,undefined)
    endif()
endfunction()
lo4_enable_sanitizers(nexy_lo4)

add_executable(lo4_tests tests/test_main.cpp)
target_link_libraries(lo4_tests PRIVATE nexy_lo4)
target_compile_features(lo4_tests PRIVATE cxx_std_20)
target_compile_options(lo4_tests PRIVATE -Wall -Wextra -Wshadow -Wconversion -Werror)
lo4_enable_sanitizers(lo4_tests)

add_executable(lo4_property_tests tests/property_main.cpp)
target_link_libraries(lo4_property_tests PRIVATE nexy_lo4)
target_compile_features(lo4_property_tests PRIVATE cxx_std_20)
target_compile_options(lo4_property_tests PRIVATE -Wall -Wextra -Wshadow -Wconversion -Werror)
lo4_enable_sanitizers(lo4_property_tests)

add_executable(lo4_example examples/integration_example.cpp)
target_link_libraries(lo4_example PRIVATE nexy_lo4)
target_compile_features(lo4_example PRIVATE cxx_std_20)
target_compile_options(lo4_example PRIVATE -Wall -Wextra -Wshadow -Wconversion -Werror)
lo4_enable_sanitizers(lo4_example)

include(CTest)
if(BUILD_TESTING)
    add_test(NAME lo4_tests COMMAND lo4_tests)
    add_test(NAME lo4_property_tests COMMAND lo4_property_tests)
endif()
