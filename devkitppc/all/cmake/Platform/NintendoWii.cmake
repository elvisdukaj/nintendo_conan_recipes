# -----------------------------------------------------------------------------
# Platform configuration

cmake_minimum_required(VERSION 3.13)
include_guard(GLOBAL)

# Platform identification flags
set(NINTENDO_WII TRUE)

# Inherit libogc platform configuration
include(Platform/Generic-dkP)

