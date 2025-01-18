cmake_minimum_required(VERSION 3.13)

if("${CMAKE_SYSTEM_NAME}" STREQUAL "NintendoWii")
    set(OGC_CONSOLE wii)
    set(OGC_SUBDIR wii)
    set(OGC_MACHINE rvl)
elseif("${CMAKE_SYSTEM_NAME}" STREQUAL "NintendoGameCube")
    set(OGC_CONSOLE gamecube)
    set(OGC_SUBDIR cube)
    set(OGC_MACHINE ogc)
else()
    message(FATAL_ERROR "Unsupported libogc platform")
endif()

# Import devkitPPC toolchain
include(${CMAKE_CURRENT_LIST_DIR}/devkitPPC.cmake)

set(OGC_ROOT ${DEVKITPRO}/libogc)
set(DKP_INSTALL_PREFIX_INIT ${DEVKITPRO}/portlibs/${OGC_CONSOLE})

find_program(ELF2DOL_EXE NAMES elf2dol HINTS "/opt/devkitpro/tools/bin")
# find_program(GCDSPTOOL_EXE NAMES gcdsptool HINTS "${DEVKITPRO}/tools/bin")
# find_program(GXTEXCONV_EXE NAMES gxtexconv HINTS "${DEVKITPRO}/tools/bin")
