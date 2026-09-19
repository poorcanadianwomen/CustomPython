# CustomPython Platform Build for CPython
# This builds the CPython interpreter for CustomPython OS

cmake_minimum_required(VERSION 3.20)
project(cpython_custompython C)

# Get the source directory (root of CustomPython project)
get_filename_component(CPYTHON_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../.." ABSOLUTE)

# Set C standard
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Include platform config
include(${CMAKE_CURRENT_SOURCE_DIR}/../../cmake/CustomPythonOS.cmake)

# Python version
set(PYTHON_VERSION "3.16.0")
set(PYTHON_MAJOR_VERSION 3)
set(PYTHON_MINOR_VERSION 16)
set(PYTHON_MICRO_VERSION 0)

# Include directories
set(CPYTHON_INCLUDE_DIRS
    ${CPYTHON_ROOT}/Include
    ${CPYTHON_ROOT}/Include/cpythonos
    ${CPYTHON_ROOT}/Include/internal
    ${CPYTHON_ROOT}/Include/internal/mimalloc
    ${CMAKE_CURRENT_BINARY_DIR}
)

# Core Python source files (minimal set for CustomPython)
set(PYTHON_CORE_SOURCES
    # Parser
    ${CPYTHON_ROOT}/Parser/token.c
    ${CPYTHON_ROOT}/Parser/pegen.c
    ${CPYTHON_ROOT}/Parser/pegen_errors.c
    ${CPYTHON_ROOT}/Parser/action_helpers.c
    ${CPYTHON_ROOT}/Parser/parser.c
    ${CPYTHON_ROOT}/Parser/string_parser.c
    ${CPYTHON_ROOT}/Parser/peg_api.c
    ${CPYTHON_ROOT}/Parser/lexer/lexer.c
    ${CPYTHON_ROOT}/Parser/lexer/number.c
    ${CPYTHON_ROOT}/Parser/lexer/state.c
    ${CPYTHON_ROOT}/Parser/lexer/string.c
    ${CPYTHON_ROOT}/Parser/tokenizer/cursor.c
    ${CPYTHON_ROOT}/Parser/tokenizer/decoder.c
    ${CPYTHON_ROOT}/Parser/tokenizer/api.c
    ${CPYTHON_ROOT}/Parser/tokenizer/reader.c
    ${CPYTHON_ROOT}/Parser/tokenizer/source.c
    ${CPYTHON_ROOT}/Parser/tokenizer/helpers.c
    ${CPYTHON_ROOT}/Parser/myreadline.c

    # Python core
    ${CPYTHON_ROOT}/Python/ceval.c
    ${CPYTHON_ROOT}/Python/compile.c
    ${CPYTHON_ROOT}/Python/flowgraph.c
    ${CPYTHON_ROOT}/Python/assemble.c
    ${CPYTHON_ROOT}/Python/ast.c
    ${CPYTHON_ROOT}/Python/ast_unparse.c
    ${CPYTHON_ROOT}/Python/import.c
    ${CPYTHON_ROOT}/Python/importdl.c
    ${CPYTHON_ROOT}/Python/pythonrun.c
    ${CPYTHON_ROOT}/Python/pylifecycle.c
    ${CPYTHON_ROOT}/Python/pystate.c
    ${CPYTHON_ROOT}/Python/sysmodule.c
    ${CPYTHON_ROOT}/Python/ceval_gil.c
    ${CPYTHON_ROOT}/Python/gc.c
    ${CPYTHON_ROOT}/Python/gc_gil.c
    ${CPYTHON_ROOT}/Python/traceback.c
    ${CPYTHON_ROOT}/Python/specialize.c
    ${CPYTHON_ROOT}/Python/instrumentation.c
    ${CPYTHON_ROOT}/Python/getversion.c
    ${CPYTHON_ROOT}/Python/symtable.c
    ${CPYTHON_ROOT}/Python/codeobject.c
    ${CPYTHON_ROOT}/Python/optimizer.c
    ${CPYTHON_ROOT}/Python/optimizer_analysis.c
    ${CPYTHON_ROOT}/Python/optimizer_symbols.c
    ${CPYTHON_ROOT}/Python/crossinterp.c
    ${CPYTHON_ROOT}/Python/frame.c
    ${CPYTHON_ROOT}/Python/genobject.c
    ${CPYTHON_ROOT}/Python/modsupport.c
    ${CPYTHON_ROOT}/Python/structmember.c
    ${CPYTHON_ROOT}/Python/marshal.c
    ${CPYTHON_ROOT}/Python/errors.c
    ${CPYTHON_ROOT}/Python/hamt.c
    ${CPYTHON_ROOT}/Python/initconfig.c
    ${CPYTHON_ROOT}/Python/preconfig.c
    ${CPYTHON_ROOT}/Python/pathconfig.c
    ${CPYTHON_ROOT}/Python/getpath.c
    ${CPYTHON_ROOT}/Python/thread.c
    ${CPYTHON_ROOT}/Python/fileutils.c
    ${CPYTHON_ROOT}/Python/dynamic_annotations.c
    ${CPYTHON_ROOT}/Python/parking_lot.c
    ${CPYTHON_ROOT}/Python/lock.c
    ${CPYTHON_ROOT}/Python/qsbr.c
    ${CPYTHON_ROOT}/Python/pyarena.c
    ${CPYTHON_ROOT}/Python/pytime.c
    ${CPYTHON_ROOT}/Python/bootstrap_hash.c
    ${CPYTHON_ROOT}/Python/frozenmain.c
    ${CPYTHON_ROOT}/Python/atexit.c
    ${CPYTHON_ROOT}/Python/call.c
    ${CPYTHON_ROOT}/Python/dictobject.c
    ${CPYTHON_ROOT}/Python/listobject.c
    ${CPYTHON_ROOT}/Python/tupleobject.c
    ${CPYTHON_ROOT}/Python/unicodeobject.c
    ${CPYTHON_ROOT}/Python/longobject.c
    ${CPYTHON_ROOT}/Python/floatobject.c
    ${CPYTHON_ROOT}/Python/bytesobject.c
    ${CPYTHON_ROOT}/Python/bytearrayobject.c
    ${CPYTHON_ROOT}/Python/boolobject.c
    ${CPYTHON_ROOT}/Python/complexobject.c
    ${CPYTHON_ROOT}/Python/rangeobject.c
    ${CPYTHON_ROOT}/Python/sliceobject.c
    ${CPYTHON_ROOT}/Python/cellobject.c
    ${CPYTHON_ROOT}/Python/funcobject.c
    ${CPYTHON_ROOT}/Python/classobject.c
    ${CPYTHON_ROOT}/Python/methodobject.c
    ${CPYTHON_ROOT}/Python/moduleobject.c
    ${CPYTHON_ROOT}/Python/namespaceobject.c
    ${CPYTHON_ROOT}/Python/weakrefobject.c
    ${CPYTHON_ROOT}/Python/descrobject.c
    ${CPYTHON_ROOT}/Python/enumobject.c
    ${CPYTHON_ROOT}/Python/iterobject.c
    ${CPYTHON_ROOT}/Python/setobject.c
    ${CPYTHON_ROOT}/Python/eval.c
    ${CPYTHON_ROOT}/Python/run.c
    ${CPYTHON_ROOT}/Python/bltinmodule.c
    ${CPYTHON_ROOT}/Python/builtinmodule.c
    ${CPYTHON_ROOT}/Python/bytecodes.c
    ${CPYTHON_ROOT}/Python/codecs.c
    ${CPYTHON_ROOT}/Python/compile.c
    ${CPYTHON_ROOT}/Python/context.c

    # Objects
    ${CPYTHON_ROOT}/Objects/object.c
    ${CPYTHON_ROOT}/Objects/typeobject.c
    ${CPYTHON_ROOT}/Objects/abstract.c
    ${CPYTHON_ROOT}/Objects/boolobject.c
    ${CPYTHON_ROOT}/Objects/bytesobject.c
    ${CPYTHON_ROOT}/Objects/bytearrayobject.c
    ${CPYTHON_ROOT}/Objects/complexobject.c
    ${CPYTHON_ROOT}/Objects/dictobject.c
    ${CPYTHON_ROOT}/Objects/floatobject.c
    ${CPYTHON_ROOT}/Objects/frameobject.c
    ${CPYTHON_ROOT}/Objects/funcobject.c
    ${CPYTHON_ROOT}/Objects/genobject.c
    ${CPYTHON_ROOT}/Objects/listobject.c
    ${CPYTHON_ROOT}/Objects/longobject.c
    ${CPYTHON_ROOT}/Objects/memoryobject.c
    ${CPYTHON_ROOT}/Objects/methodobject.c
    ${CPYTHON_ROOT}/Objects/moduleobject.c
    ${CPYTHON_ROOT}/Objects/namespaceobject.c
    ${CPYTHON_ROOT}/Objects/odictobject.c
    ${CPYTHON_ROOT}/Objects/rangeobject.c
    ${CPYTHON_ROOT}/Objects/setobject.c
    ${CPYTHON_ROOT}/Objects/sliceobject.c
    ${CPYTHON_ROOT}/Objects/structseq.c
    ${CPYTHON_ROOT}/Objects/tupleobject.c
    ${CPYTHON_ROOT}/Objects/typeobject.c
    ${CPYTHON_ROOT}/Objects/unicodeobject.c
    ${CPYTHON_ROOT}/Objects/weakrefobject.c
    ${CPYTHON_ROOT}/Objects/exceptions.c
    ${CPYTHON_ROOT}/Objects/obmalloc.c
    ${CPYTHON_ROOT}/Objects/accu.c
    ${CPYTHON_ROOT}/Objects/capsule.c
    ${CPYTHON_ROOT}/Objects/cellobject.c
    ${CPYTHON_ROOT}/Objects/classobject.c
    ${CPYTHON_ROOT}/Objects/codeobject.c
    ${CPYTHON_ROOT}/Objects/enumobject.c
    ${CPYTHON_ROOT}/Objects/iterobject.c
    ${CPYTHON_ROOT}/Objects/logic.c
    ${CPYTHON_ROOT}/Objects/patchrange.c
    ${CPYTHON_ROOT}/Objects/stringlib/unicode_format.c
    ${CPYTHON_ROOT}/Objects/structmember.c

    # Modules (built-in)
    ${CPYTHON_ROOT}/Modules/config.c
    ${CPYTHON_ROOT}/Modules/gcmodule.c
    ${CPYTHON_ROOT}/Modules/getbuildinfo.c
    ${CPYTHON_ROOT}/Modules/getpath.c
    ${CPYTHON_ROOT}/Modules/main.c
    ${CPYTHON_ROOT}/Modules/mathmodule.c
    ${CPYTHON_ROOT}/Modules/cmathmodule.c
    ${CPYTHON_ROOT}/Modules/errnomodule.c
    ${CPYTHON_ROOT}/Modules/_io/_iomodule.c
    ${CPYTHON_ROOT}/Modules/_io/fileio.c
    ${CPYTHON_ROOT}/Modules/_io/bytesio.c
    ${CPYTHON_ROOT}/Modules/_io/bufferedio.c
    ${CPYTHON_ROOT}/Modules/_io/textio.c
    ${CPYTHON_ROOT}/Modules/_io/stringio.c
    ${CPYTHON_ROOT}/Modules/_io/zlibmodule.c
    ${CPYTHON_ROOT}/Modules/_json.c
    ${CPYTHON_ROOT}/Modules/_sre/sre.c
    ${CPYTHON_ROOT}/Modules/_collectionsmodule.c
    ${CPYTHON_ROOT}/Modules/_functoolsmodule.c
    ${CPYTHON_ROOT}/Modules/_operator.c
    ${CPYTHON_ROOT}/Modules/itertoolsmodule.c
    ${CPYTHON_ROOT}/Modules/_abc.c
    ${CPYTHON_ROOT}/Modules/_weakref.c
    ${CPYTHON_ROOT}/Modules/_codecsmodule.c
    ${CPYTHON_ROOT}/Modules/_symtable.c
    ${CPYTHON_ROOT}/Modules/symtablemodule.c
    ${CPYTHON_ROOT}/Modules/_tracemalloc.c
    ${CPYTHON_ROOT}/Modules/_suggestions.c
    ${CPYTHON_ROOT}/Modules/faulthandler.c
    ${CPYTHON_ROOT}/Modules/signalmodule.c
    ${CPYTHON_ROOT}/Modules/_threadmodule.c
    ${CPYTHON_ROOT}/Modules/timemodule.c
    ${CPYTHON_ROOT}/Modules/_datetimemodule.c
    ${CPYTHON_ROOT}/Modules/_pickle.c
    ${CPYTHON_ROOT}/Modules/_randommodule.c
    ${CPYTHON_ROOT}/Modules/_struct.c
    ${CPYTHON_ROOT}/Modules/arraymodule.c
    ${CPYTHON_ROOT}/Modules/_bisectmodule.c
    ${CPYTHON_ROOT}/Modules/_csv.c
    ${CPYTHON_ROOT}/Modules/_heapqmodule.c
    ${CPYTHON_ROOT}/Modules/_queuemodule.c
    ${CPYTHON_ROOT}/Modules/_interpretersmodule.c
    ${CPYTHON_ROOT}/Modules/_interpchannelsmodule.c
    ${CPYTHON_ROOT}/Modules/_interpqueuesmodule.c
    ${CPYTHON_ROOT}/Modules/_typingmodule.c
    ${CPYTHON_ROOT}/Modules/_stat.c
    ${CPYTHON_ROOT}/Modules/_typesmodule.c

    # Entry point
    ${CPYTHON_ROOT}/Programs/python.c
)

# Remove files that won't compile on CustomPython OS
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*dynload_shlib.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*dynload_win.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*posixmodule.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*posixsubprocess.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*fcntlmodule.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*mmapmodule.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*selectmodule.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*pollmodule.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*socketmodule.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*sslmodule.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*_hashlib.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*_sqlite3.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*_ctypes.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*_curses.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*_tkinter.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*_decimal.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*_uuid.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*_bz2.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*_lzma.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*_zstd.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*zlibmodule.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*_dbm.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*_gdbm.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*readline.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*_scproxy.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*resource.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*_posixshmem.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*syslogmodule.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*termios.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*grpmodule.*")
list(FILTER PYTHON_CORE_SOURCES EXCLUDE REGEX ".*pwdmodule.*")

# Create CPython library
add_library(cpython STATIC
    ${PYTHON_CORE_SOURCES}
)

# Include directories
target_include_directories(cpython PUBLIC
    ${CPYTHON_INCLUDE_DIRS}
)

# Compile definitions
target_compile_definitions(cpython PRIVATE
    Py_BUILD_CORE
    Py_BUILD_CORE_BUILTIN
    PYTHONPATH=""
    PYTHONHOME=""
    VERSION="${PYTHON_VERSION}"
    PLAT="custompython-x86_64"
    SOABI="cpython-316-custompython"
    ABIFLAGS=""
    MULTIARCH_CPPFLAGS=""
)

# Compiler flags
target_compile_options(cpython PRIVATE
    -Wno-unused-parameter
    -Wno-missing-field-initializers
    -Wno-sign-compare
)

# Create executable
add_executable(cpython_custompython
    Programs/python.c
)

target_link_libraries(cpython_custompython PRIVATE cpython)

# Install
install(TARGETS cpython_custompython RUNTIME DESTINATION bin)
