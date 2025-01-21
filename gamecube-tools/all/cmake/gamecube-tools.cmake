cmake_minimum_required(VERSION 3.13)
include_guard(GLOBAL)

find_program(ELF2DOL_EXE NAMES elf2dol)
find_program(GCDSPTOOL_EXE NAMES gcdsptool)
find_program(GXTEXCONV_EXE NAMES gxtexconv)

# Platform-specific helper utilities
function(__dkp_target_derive_name outvar target suffix)
	get_target_property(dir ${target} BINARY_DIR)
	get_target_property(outname ${target} OUTPUT_NAME)
	if(NOT outname)
		set(outname "${target}")
	endif()

	set(${outvar} "${dir}/${outname}${suffix}" PARENT_SCOPE)
endfunction()

function(__dkp_set_target_file target)
	if (NOT ${ARGC} GREATER 1)
		message(FATAL_ERROR "dkp_set_target_file: must provide at least one input file")
	endif()

	set_target_properties(${target} PROPERTIES DKP_FILE "${ARGN}")
endfunction()

function(ogc_create_dol target)
    if (NOT ELF2DOL_EXE)
        message(FATAL_ERROR "Could not find elf2dol: try installing gamecube-tools")
    endif()

    __dkp_target_derive_name(DOL_OUTPUT ${target} ".dol")
    add_custom_command(TARGET ${target} POST_BUILD
        COMMAND "${ELF2DOL_EXE}" "$<TARGET_FILE:${target}>" "${DOL_OUTPUT}"
        BYPRODUCTS "${DOL_OUTPUT}"
        COMMENT "Converting ${target} to .dol format"
        VERBATIM
    )
    __dkp_set_target_file(${target} "${DOL_OUTPUT}")
endfunction()
