cmake_minimum_required(VERSION 3.13)

if(CMAKE_HOST_WIN32)
	message(FATAL_ERROR "CMake must be installed and launched from msys2: pacman -S cmake")
endif()

if(NOT DEFINED ENV{DEVKITPRO})
  message(FATAL_ERROR "DEVKITPRO variable not defined")
endif()

set(DEVKITPRO "$ENV{DEVKITPRO}")

list(APPEND CMAKE_MODULE_PATH "${DEVKITPRO}/cmake")
