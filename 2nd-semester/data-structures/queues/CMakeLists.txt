cmake_minimum_required(VERSION 3.17)
project(DataStructures_Queues CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(circular_queue_display circular_queue_display.cpp)
add_executable(queue_reverse          queue_reverse.cpp)
