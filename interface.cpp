#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "diff-match-patch-cpp-stl/diff_match_patch.h"

struct BytesShim {
    static const char* PyArgFormat; // set below
    typedef Py_buffer PY_ARG_TYPE;
    typedef std::string STL_STRING_TYPE;

    // There are no element width issues for bytes.
    static bool check_width(const Py_buffer& value) {
        return true;
    }

    // Extract the bytes data.
    static std::string to_string(Py_buffer& value) {
        auto buffer = (char*)malloc(value.len + 1);
        PyBuffer_ToContiguous(buffer, &value, value.len, 'C');
        PyBuffer_Release(&value);
        auto s = std::string(buffer, value.len);
        free(buffer);
        return s;
    }

    // Create PyString from underlying char array
    static PyObject* from_string(std::string& value) {
        return PyBytes_FromStringAndSize(value.data(), value.size());
    }
};

const char* BytesShim::PyArgFormat = "s*";

struct UnicodeShim {
    static const char* PyArgFormat; // set below
    typedef PyObject* PY_ARG_TYPE;
    typedef std::wstring STL_STRING_TYPE;

    static bool check_width(PyObject* value) {
        // Return whether any four-byte Unicode characters exist
        // and the platform's wchar_t type only is two bytes, e.g.
        // on Windows.
        return PyUnicode_MAX_CHAR_VALUE(value) <= WCHAR_MAX;
    }

    // Convert PyObject* to std::wstring....
    static std::wstring to_string(PyObject* value) {
        Py_ssize_t size;
        wchar_t* str = PyUnicode_AsWideCharString(value, &size);
        std::wstring string = std::wstring(str, size);
        PyMem_Free(str);
        return string;
    }

    static PyObject* from_string(std::wstring value) {
        return PyUnicode_FromWideChar(value.data(), value.size());
    }
};
const char* UnicodeShim::PyArgFormat = "U";

// COMPUTATIONAL FUNCTIONS

template <class Shim>
static PyObject *
diff_match_patch__diff__impl(PyObject *self, PyObject *args, PyObject *kwargs)
{
    typename Shim::PY_ARG_TYPE a, b;
    float timelimit = 0.0;
    int checklines = 1;
    char* cleanupMode = NULL;
    int counts_only = 1;
    int as_patch = 0;
    char format_spec[64];

    static char *kwlist[] = {
        strdup("left_document"),
        strdup("right_document"),
        strdup("timelimit"),
        strdup("checklines"),
        strdup("cleanup"),
        strdup("counts_only"),
        strdup("as_patch"),
        NULL };

    sprintf(format_spec, "%s%s|fbzbb", Shim::PyArgFormat, Shim::PyArgFormat);
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, format_spec, kwlist,
                                     &a, &b,
                                     &timelimit, &checklines, &cleanupMode,
                                     &counts_only, &as_patch))
        return NULL;

    auto a_str = Shim::to_string(a),
         b_str = Shim::to_string(b);

    // On Windows, wstring is based on the two-byte wchar_t,
    // which is smaller than the four-byte Py_UCS4 that is
    // the basis for Python strings. As a result, high-code-point
    // characters will be split into two wchar_t characters,
    // and the diff will return insertion/deletion counts
    // that don't line up with the input string. Raise an
    // exception if this would occur.
    if (!Shim::check_width(a) || !Shim::check_width(b)) {
        PyErr_SetString(PyExc_RuntimeError, "String contains high-code-point characters that cannot be represented natively on this platform.");
        return NULL;
    }

    PyObject *ret = PyList_New(0);

    typedef diff_match_patch<typename Shim::STL_STRING_TYPE> DMP;
    DMP dmp;

    PyObject *opcodes[3];
    opcodes[dmp.DELETE] = PyUnicode_FromString("-");
    opcodes[dmp.INSERT] = PyUnicode_FromString("+");
    opcodes[dmp.EQUAL] = PyUnicode_FromString("=");

    typename DMP::Diffs diff;

    Py_BEGIN_ALLOW_THREADS /* RELEASE THE GIL */

    dmp.Diff_Timeout = timelimit;
    diff = dmp.diff_main(a_str, b_str, checklines);

    if (cleanupMode == NULL || strcmp(cleanupMode, "Semantic") == 0)
        dmp.diff_cleanupSemantic(diff);
    else if (strcmp(cleanupMode, "Efficiency") == 0)
        dmp.diff_cleanupEfficiency(diff);

    Py_END_ALLOW_THREADS /* ACQUIRE THE GIL */

    if (as_patch) {
        typename DMP::Patches patch = dmp.patch_make(a_str, diff);
        typename Shim::STL_STRING_TYPE patch_str = dmp.patch_toText(patch);

        return Shim::from_string(patch_str);
    }

    typename std::list<typename DMP::Diff>::const_iterator entryiter;
    for (entryiter = diff.begin(); entryiter != diff.end(); entryiter++) {
        typename DMP::Diff entry = *entryiter;

        PyObject* tuple = PyTuple_New(2);

        Py_INCREF(opcodes[entry.operation]); // we're going to reuse the object, so don't let SetItem steal the reference
        PyTuple_SetItem(tuple, 0, opcodes[entry.operation]);

        if (counts_only)
            PyTuple_SetItem(tuple, 1, PyLong_FromLong(entry.text.length()));
        else
            PyTuple_SetItem(tuple, 1, Shim::from_string(entry.text));

        PyList_Append(ret, tuple);
        Py_DECREF(tuple); // the list owns a reference now
    }

    // We're left with one extra reference.
    Py_DECREF(opcodes[dmp.DELETE]);
    Py_DECREF(opcodes[dmp.INSERT]);
    Py_DECREF(opcodes[dmp.EQUAL]);

    return ret;
}

template <class Shim>
static PyObject *
diff_match_patch__match__impl(PyObject *self, PyObject *args, PyObject *kwargs)
{
    typename Shim::PY_ARG_TYPE pattern, text;
    int loc;
    int match_distance = 1000;
    int match_maxbits = 32;
    float match_threshold = 0.5;
    char format_spec[64];

    static char *kwlist[] = {
        strdup("text"),
        strdup("pattern"),
        strdup("loc"),
        strdup("match_distance"),
        strdup("match_maxbits"),
        strdup("match_threshold"),
        NULL };

    sprintf(format_spec, "%s%si|iif", Shim::PyArgFormat, Shim::PyArgFormat);
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, format_spec, kwlist,
                                     &text, &pattern, &loc,
                                     &match_distance, &match_maxbits, &match_threshold)) {
        return NULL;
    }

    auto pattern_str = Shim::to_string(pattern),
         text_str = Shim::to_string(text);

    if (!Shim::check_width(pattern) || !Shim::check_width(text)) {
        PyErr_SetString(PyExc_RuntimeError, "String contains high-code-point characters that cannot be represented natively on this platform.");
        return NULL;
    }

    typedef diff_match_patch<typename Shim::STL_STRING_TYPE> DMP;
    DMP dmp;

    dmp.Match_Distance = match_distance;
    dmp.Match_MaxBits = match_maxbits;
    dmp.Match_Threshold = match_threshold;

    try {
        int index = dmp.match_main(text_str, pattern_str, loc);
        return Py_BuildValue("i", index);
    } catch (std::exception& e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    } catch (typename Shim::STL_STRING_TYPE& s) {
        PyErr_SetObject(PyExc_RuntimeError, Shim::from_string(s));
        return NULL;
    }
}

// WRAPPER FUNCTIONS THAT DETERMINE WHETHER UNICODE OR BYTES ARE PASSED

static PyObject *
diff_match_patch__diff(PyObject *self, PyObject *args, PyObject *kwargs)
{
    // Check if the first argument is a Unicode object, and if so, run
    // the Unicode version of the method. Otherwise run the bytes version.
    PyObject* first_arg;
    if (PyTuple_Size(args) > 0 && (first_arg = PyTuple_GetItem(args, 0)))
        if (PyUnicode_Check(first_arg))
            return diff_match_patch__diff__impl<UnicodeShim>(self, args, kwargs);
    return diff_match_patch__diff__impl<BytesShim>(self, args, kwargs);
}

static PyObject *
diff_match_patch__match(PyObject *self, PyObject *args, PyObject *kwargs)
{
    // Check if the first argument is a Unicode object, and if so, run
    // the Unicode version of the method. Otherwise run the bytes version.
    PyObject* first_arg;
    if (PyTuple_Size(args) > 0 && (first_arg = PyTuple_GetItem(args, 0)))
        if (PyUnicode_Check(first_arg))
            return diff_match_patch__match__impl<UnicodeShim>(self, args, kwargs);
    return diff_match_patch__match__impl<BytesShim>(self, args, kwargs);
}

// EXTENSION MODULE METADATA

static PyMethodDef MyMethods[] = {
    {"diff", (PyCFunction)diff_match_patch__diff, METH_VARARGS|METH_KEYWORDS,
    "Compute the difference between two strings or bytes. Returns a list of tuples (OP, LEN)."},
    {"match", (PyCFunction)diff_match_patch__match, METH_VARARGS|METH_KEYWORDS,
    "Locate the best instance of 'pattern' in 'text' near 'loc'. Returns -1 if no match found."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef mymodule = {
   PyModuleDef_HEAD_INIT,
   "fast_diff_match_patch",   /* name of module */
   NULL, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   MyMethods
};

PyMODINIT_FUNC
PyInit_fast_diff_match_patch(void)
{
    auto module = PyModule_Create(&mymodule);
    PyModule_AddIntConstant(module, "CHAR_WIDTH", sizeof(UnicodeShim::STL_STRING_TYPE::value_type));
    return module;
}
