# venvpp2
Welcome to venvpp2!

This project is an evolution of my previous [venvpp](https://github.com/TeiaCare/venvpp).

The main enhancements with respect to its predecessor are:
[Conan v2](https://conan.io/) and [CMake v4](https://cmake.org/) with the usage of *CMakePresets* as first class citizens replacing the older custom Python scripts to addressing Configure, Build, Install, Test and Package the project.

---

## Getting started
In order to spin up a fresh C++ development environment in your local repository just run the following command.

The setup scripts resolve their requirements file relative to the script itself, so they can be invoked from any working directory.

### Setup Virtual Environment

```bash
# MacOS/Linux
scripts/env/setup.sh
source .venv/bin/activate

# Windows
scripts/env/setup.bat
.venv\Scripts\activate.bat
```

The virtual environment installs the toolchain pinned in `scripts/requirements.txt`:
`cmake`, `conan`, `ninja`, `clang-format`, `pre-commit` and `gcovr` (used by the coverage tool).

## Install Conan packages
```bash
# Install packages and create CMakePresets.json + CMake toolchain file
conan install . -b=missing -pr:a=profiles/linux-clang -s build_type=Debug
```

Profiles for the supported toolchains live under `profiles/` (`linux-clang`, `linux-gcc`, `macos-arm64`, `macos-x64`, `windows-msvc`).

## Configure, Build and Install
```bash
# CMake configure
cmake --preset conan-debug

# CMake build
cmake --build build/Debug

# CMake install
cmake --install build/Debug

# Run
install/venvpp2_example
```

## Lockfile
```bash
# Create lockfile
conan lock create .

# Install using lockfile
conan install . --lockfile=conan.lock --output-folder=build/Release
```

---

## Build & QA tools

The `tools/` directory ships a set of shared Python helpers that wrap the most common
build, test and analysis commands. They share a thin `command.py` runner and are designed
to be reused both locally and in CI.

| Script | Purpose |
| --- | --- |
| `run_unit_tests.py` | Run unit tests via `ctest` (default) or directly via the GoogleTest binary, emitting a JUnit XML report. |
| `run_coverage.py` | Generate Cobertura XML and HTML coverage reports with `gcovr` (supports `gcc` and `clang`/`apple-clang`). |
| `run_sanitizer.py` | Run a binary under AddressSanitizer (`--address_sanitizer`) or ThreadSanitizer (`--thread_sanitizer`). |
| `run_valgrind.py` | Run a binary under Valgrind `memcheck` or `callgrind`. |
| `install_valgrind.sh` | Build & cache Valgrind from source (used by CI). |
| `run_benchmarks.py` | Execute a Google Benchmark binary and dump JSON results. |
| `run_examples.py` | Discover and execute every executable found in an examples directory. |
| `run_clang_format.py` | Format C/C++ sources in parallel using `clang-format -style=file`. |
| `run_clang_tidy.py` | Run `clang-tidy` checks on C/C++ sources in parallel. |
| `run_cppcheck.py` | Run `cppcheck` against the project's `compile_commands.json`. |
| `run_doxygen.py` | Generate Doxygen documentation from a given `Doxyfile`. |

Each script exposes `--help` for the full list of arguments and defaults.
