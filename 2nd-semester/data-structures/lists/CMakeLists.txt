cmake_minimum_required(VERSION 3.17)
project(DataStructures_Lists CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(linked_list_int         linked_list_int.cpp)
add_executable(linked_list_student     linked_list_student.cpp)
add_executable(linked_list_delete_all  linked_list_delete_all.cpp)
add_executable(linked_list_delete_last linked_list_delete_last.cpp)
add_executable(linked_list_filter      linked_list_filter.cpp)
