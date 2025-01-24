# Description

This repository contains a list of conan recipes that provides toolchain, tools and libraries for developing for the Nintendo Wii, Wii U and Game Cube.

Most of the code is coming from the https://devkitpro.org please consider to sponsor that project. This work wouldn't be possible without the tool provided by them.

## What is included

- `devkitppc`: this is the toolchain for targetting the Wii. It's based on GCC 14.2.
- `flock`: utility for file lock used by `libogc`
- `gamecube-tools`: utility tools for GameCube and Wii to convert from *.elf to *.dol and other small utilities
- `general-tools`: convert binary files to GCC assembly modules
- `libogc`: C Library for Wii and Gamecube homebrew
- `opengx`: OpenGL-like wrapper for Nintendo Wii/GameCube
- `libdvm`: disk and volume management library for devkitPro platforms
- `sdl2`: **EXPERIMENTAL**

# Preparation

## Conan settings

To extend conan to use new operating systems and toolchain, create `settings_user.yml` with the above content and put it in the conan home folder, usualy located in `~/.conan2/`.

```YAML
os:
  NintendoWii:
  NintendoGameCube:
compiler:
    devkitppc:
        version: ["r46.1"]
        libcxx: [libstdc++, libstdc++11]
        cppstd: [null, 98, gnu98, 11, gnu11, 14, gnu14, 17, gnu17, 20, gnu20, 23, gnu23, 26, gnu26]
        cstd: [null, 99, gnu99, 11, gnu11, 17, gnu17, 23, gnu23]
```

# conan profile

I've created the following `NintendoWii` profile. Create the file with the above content and put it on the profile folder, usualy `~/.conan2/profiles/`.

```
[settings]
os=NintendoWii
arch=ppc32be
build_type=Release
compiler=devkitppc
compiler.cppstd=23
compiler.version=r46.1
compiler.libcxx=libstdc++11
compiler.cstd=99

[tool_requires]
ninja/1.11.1
cmake/3.31.3
devkitppc/r46.1

[conf]
tools.cmake.cmaketoolchain:generator=Ninja
tools.cmake.cmake_layout:build_folder_vars=['settings.os', 'settings.arch', 'settings.compiler', 'settings.compiler.version']
tools.cmake.cmaketoolchain:extra_variables={"CMAKE_EXPORT_COMPILE_COMMANDS": "TRUE"}
```

# How to build

Be sure that the `settings_user.yml` and the `NintendoWii` profile are installed correctly.

** The build are tested only on MacOS so I cannot guarantee for Windows or Linux environmt yet. **

The order of build is important since there are dependencies between different packages.

## Build

```Bash
conan create devkitppc/all --version r46.1
conan create flock/all --version 0.4.0
conan create gamecube-tools/all --version 1.0.6
coman create general-tools/all --version 1.4.4
conan create libogc/all --version 2.10.0 --profile NintendoWii
conan create opengx/all --version 0.15.0 --profile NintendoWii  
conan create libdvm/all --version 2.0.0 --profile NintendoWii
conan create sdl/all --version 2.18.5-15 --profile NintendoWii
```

devkitppc in particular is building gcc 14.2, newlib and binutils with patches for Wii.

The build  should work on Linux, msys2 and macOS, but I've tried only on macOS. MR are welcome for different operating systems.

# Emulator

I am using the [Dolphin](https://dolphin-emu.org).

Follow the instruction [here](https://github.com/elvisdukaj/nintendo_conan_recipes/pull/11) To set the
emulator to work for homebrew applications.