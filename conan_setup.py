import argparse
import subprocess
import sys
import os

def check_env():
    if not os.getenv('VIRTUAL_ENV'):
        raise SystemError("\n========================================================"
                          "\nYou are not running inside a python virtual environment"
                          "\nConfigure and activate it as shown in the project README"
                          "\n========================================================\n")
    if not os.getenv('CONAN_HOME'):
        raise SystemError("\n========================================================"
                          "\nConan home is not properly configured"
                          "\nMake sure to run the env/setup.sh|bat script first"
                          "\n========================================================\n")

    print("CONAN_HOME:", os.getenv('CONAN_HOME'))

def parse():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("build_type", help="Debug or Release", choices=['Debug', 'Release', 'RelWithDebInfo'])
    parser.add_argument("compiler", help="Compiler name", choices=['gcc', 'clang', 'visual_studio'])
    parser.add_argument("compiler_version", help="Compiler version")
    parser.add_argument("-d", "--directories", help="Specific conanfiles directories", nargs='*', required=False)
    return parser.parse_args()

def resolve_profile(compiler):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    platform_map = {
        'gcc': 'linux-gcc',
        'clang': 'linux-clang',
        'visual_studio': 'windows-msvc',
    }
    profile_file = platform_map.get(compiler)
    if not profile_file:
        raise ValueError(f"Unknown compiler: {compiler}")

    source = os.path.join(script_dir, 'profiles', profile_file)
    if not os.path.isfile(source):
        raise FileNotFoundError(f"Profile not found: {source}")

    dest_dir = os.path.join(os.getenv("CONAN_HOME"), 'profiles')
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, profile_file)

    import shutil
    shutil.copy2(source, dest)
    print(f"Installed profile: {source} -> {dest}")
    return profile_file

def install(profile_name, build_type):
    subprocess.run([
        'conan', 'install', '.',
        '--settings', f'build_type={build_type}',
        '--profile:all', profile_name,
        '--build', 'missing'
    ], check=True)

def main():
    check_env()
    args = parse()
    profile_name = resolve_profile(args.compiler)
    install(profile_name, args.build_type)

if __name__ == '__main__':
    sys.exit(main())
