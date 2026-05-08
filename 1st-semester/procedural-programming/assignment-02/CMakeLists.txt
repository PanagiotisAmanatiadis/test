cmake_minimum_required(VERSION 3.17)
project(Assignment02 CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(${CMAKE_SOURCE_DIR}/../include)

add_executable(ex06_min_max_array    ex06_min_max_array.cpp)
add_executable(ex09_student_absences ex09_student_absences.cpp)
