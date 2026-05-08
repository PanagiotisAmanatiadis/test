cmake_minimum_required(VERSION 3.17)
project(Assignment04 CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(${CMAKE_SOURCE_DIR}/../include)

add_executable(ex01_profit_calculator ex01_profit_calculator.cpp)
add_executable(ex05_sales_report      ex05_sales_report.cpp)
add_executable(ex09_kickback_report   ex09_kickback_report.cpp)
