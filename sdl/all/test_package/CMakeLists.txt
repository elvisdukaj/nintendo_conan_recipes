cmake_minimum_required(VERSION 3.15)
project(test_package)

find_package(SDL2 REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.c)
target_link_libraries(${PROJECT_NAME} PRIVATE SDL2::SDL2main)

ogc_create_dol(${PROJECT_NAME})

