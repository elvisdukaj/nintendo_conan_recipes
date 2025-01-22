cmake_minimum_required(VERSION 3.13)

macro(__dkp_toolchain name arch triplet)
	set(${name} TRUE)

	if(NOT CMAKE_SYSTEM_VERSION)
		# Usually, this setting is unused in "non-standard" platforms.
		set(CMAKE_SYSTEM_VERSION 1)
	endif()
endmacro()
