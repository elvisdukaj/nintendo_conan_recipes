cmake_minimum_required(VERSION 3.1)
project(test_package)

add_executable(${PROJECT_NAME} test_package.cpp)

ogc_create_dol(${PROJECT_NAME})
