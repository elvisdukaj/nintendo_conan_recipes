# -----------------------------------------------------------------------------
# Generic configuration for devkitPro platforms

cmake_minimum_required(VERSION 3.13)
include_guard(GLOBAL)

# Use .elf extension for compiled binaries
set(CMAKE_EXECUTABLE_SUFFIX .elf)

# Disable shared library support
set(BUILD_SHARED_LIBS OFF CACHE INTERNAL "Shared libs not available")
set_property(GLOBAL PROPERTY TARGET_SUPPORTS_SHARED_LIBS FALSE)

# Helper macro for platform settings initialization
macro(__dkp_init_platform_settings platform)
	foreach(lang IN ITEMS C CXX ASM)
		set(CMAKE_${lang}_FLAGS_INIT "${${platform}_ARCH_SETTINGS} ${${platform}_COMMON_FLAGS}")

		if(NOT DKP_PLATFORM_BOOTSTRAP)
			set(CMAKE_${lang}_STANDARD_LIBRARIES "${${platform}_STANDARD_LIBRARIES}" CACHE STRING "" FORCE)
			set(CMAKE_${lang}_STANDARD_INCLUDE_DIRECTORIES "${${platform}_STANDARD_INCLUDE_DIRECTORIES}" CACHE STRING "")
		endif()
	endforeach()

	string(APPEND CMAKE_ASM_FLAGS_INIT " -x assembler-with-cpp")

	set(CMAKE_EXE_LINKER_FLAGS_INIT "${${platform}_ARCH_SETTINGS} ${${platform}_LINKER_FLAGS}")

	if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT AND DEFINED DKP_INSTALL_PREFIX_INIT)
		set(CMAKE_INSTALL_PREFIX "${DKP_INSTALL_PREFIX_INIT}" CACHE PATH
			"Install path prefix, prepended onto install directories." FORCE)
	endif()

	if(NOT CMAKE_LIBRARY_ARCHITECTURE)
		string(REPLACE " " ";" _dkp_arch "${${platform}_ARCH_SETTINGS}")
		if(CMAKE_POSITION_INDEPENDENT_CODE)
			list(APPEND _dkp_arch "-fPIC")
		endif()

		execute_process(
			COMMAND "${CMAKE_C_COMPILER}" ${_dkp_arch} -print-multi-directory
			OUTPUT_VARIABLE _dkp_multidir
			RESULT_VARIABLE _dkp_retval
			OUTPUT_STRIP_TRAILING_WHITESPACE
		)

		if(NOT _dkp_retval AND NOT _dkp_multidir STREQUAL ".")
			set(CMAKE_LIBRARY_ARCHITECTURE "${_dkp_multidir}" CACHE INTERNAL "abi")
			message(STATUS "Detected multilib folder: ${CMAKE_LIBRARY_ARCHITECTURE}")
		endif()
	endif()
endmacro()

# -----------------------------------------------------------------------------
# Helper utilities

# Include common devkitPro bits and pieces
include(dkp-impl-helpers)
