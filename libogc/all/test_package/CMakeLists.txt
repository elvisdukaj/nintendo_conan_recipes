cmake_minimum_required(VERSION 3.30)

project(test_package LANGUAGES C VERSION 1.0.0)

find_package(libogc REQUIRED CONFIG COMPONENTS ogc wiikeyboard)

add_executable(${PROJECT_NAME} test_package.c)

target_link_libraries(${PROJECT_NAME} PRIVATE libogc::ogc libogc::wiikeyboard)

ogc_create_dol(${PROJECT_NAME})
