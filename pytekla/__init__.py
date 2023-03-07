import os
import sys

import clr
from .config.config import _read_tekla_path
import System

BASE_PATH = _read_tekla_path()

try:
    dlls = [
        "Tekla.Structures.dll",
        "Tekla.Structures.Plugins.dll",
        "Tekla.Structures.Model.dll",
        "Tekla.Structures.DataType.dll",
        "Tekla.Structures.Geometry3d.Compatibility.dll",
        "Tekla.Structures.Dialog.dll",
        "Tekla.Structures.Analysis.dll",
        "Tekla.Structures.Catalogs.dll",
        "Tekla.Structures.Drawing.dll",
    ]

    for dll in dlls:
        clr.AddReference(os.path.join(BASE_PATH, dll))

    from .wrappers import *
except System.IO.FileNotFoundException:
    sys.stderr.write(
        "\033[91m"
        + 'Please set a valid path to the Tekla Structures bin folder before using this library.\nUse "pytekla.config.set_tekla_path"\n.'
        + "\033[0m"
    )
