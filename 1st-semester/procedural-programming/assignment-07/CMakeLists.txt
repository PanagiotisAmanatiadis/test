cmake_minimum_required(VERSION 3.17)
project(Assignment07 CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(${CMAKE_SOURCE_DIR}/../include)

add_executable(ex02_weekly_salary  ex02_weekly_salary.cpp)
add_executable(ex08_car_rental     ex08_car_rental.cpp)
add_executable(ex09_extract_digits ex09_extract_digits.cpp)
