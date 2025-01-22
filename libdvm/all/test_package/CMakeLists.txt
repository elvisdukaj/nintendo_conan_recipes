cmake_minimum_required(VERSION 3.30)

project(test_package LANGUAGES C VERSION 1.0.0)

find_package(libdvm REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.c)

target_link_libraries(${PROJECT_NAME} PRIVATE libdvm::libdvm)

ogc_create_dol(${PROJECT_NAME})
