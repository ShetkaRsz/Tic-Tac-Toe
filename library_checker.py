######################################################################
#                             Libraries                              #
######################################################################


from pip._internal import pip


######################################################################
#                             Functions                              #
######################################################################


def try_to_download(library_name: str) -> str:
    try:
        __import__(library_name)
        return f"You have already installed {library_name}!"
    except ImportError:
        pip.main(['install', library_name])
        return f"{library_name} has been succesfully downloaded!"


def download_libraries() -> None:
    print("", *[f"{n + 1}) {try_to_download(lib)}" for n, lib in enumerate(["pygame", "numba", "sys", "itertools", "copy"])], "", sep="\n")


######################################################################
#                  Made by: @Ice_Lightning_Strike                    #
######################################################################