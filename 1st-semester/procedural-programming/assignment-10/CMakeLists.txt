cmake_minimum_required(VERSION 3.17)
project(Assignment10 CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(${CMAKE_SOURCE_DIR}/../include)

add_executable(ex03_multiplication_table ex03_multiplication_table.cpp)
add_executable(ex09_space_after_punct    ex09_space_after_punct.cpp)
