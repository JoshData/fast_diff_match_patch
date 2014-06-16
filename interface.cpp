#include <Python.h>

#include "diff-match-patch-cpp-stl/diff_match_patch.h"

#if PY_MAJOR_VERSION == 3
    // Upgrade these types.
    #define PyString_FromString PyUnicode_FromString
    #define PyString_FromStringAndSize PyUnicode_FromStringAndSize
    #define PyInt_FromLong PyLong_FromLong
#endif

template <class STORAGE_TYPE, char FMTSPEC, class CPPTYPE, class PYTYPE>
static PyObject *
diff_match_patch_diff(PyObject *self, PyObject *args, PyObject *kwargs)
{
    STORAGE_TYPE *a, *b;
    float timelimit = 0.0;
    int checklines = 1;
    int counts_only = 1;
    char format_spec[7];

    static char *kwlist[] = { strdup("left_document"), strdup("right_document"), strdup("timelimit"), strdup("checklines"), strdup("counts_only"), NULL };

    sprintf(format_spec, "%c%c|fbb", FMTSPEC, FMTSPEC);
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, format_spec, kwlist,
                                     &a, &b, &timelimit, &checklines, &counts_only))
        return NULL;
    
    PyObject *ret = PyList_New(0);
    
    typedef diff_match_patch<CPPTYPE> DMP;
    DMP dmp;

    PyObject *opcodes[3];
    opcodes[dmp.DELETE] = PyString_FromString("-");
    opcodes[dmp.INSERT] = PyString_FromString("+");
    opcodes[dmp.EQUAL] = PyString_FromString("=");
    
    dmp.Diff_Timeout = timelimit;
    typename DMP::Diffs diff = dmp.diff_main(a, b, checklines);
    typename std::list<typename DMP::Diff>::const_iterator entryiter;
    for (entryiter = diff.begin(); entryiter != diff.end(); entryiter++) {
        typename DMP::Diff entry = *entryiter;

        PyObject* tuple = PyTuple_New(2);

        Py_INCREF(opcodes[entry.operation]); // we're going to reuse the object, so don't let SetItem steal the reference
        PyTuple_SetItem(tuple, 0, opcodes[entry.operation]);

        if (counts_only)
            PyTuple_SetItem(tuple, 1, PyInt_FromLong(entry.text.length()));
        else if (FMTSPEC == 'u')
            PyTuple_SetItem(tuple, 1, PyUnicode_FromUnicode((Py_UNICODE*)entry.text.data(), entry.text.size()));
        else
            PyTuple_SetItem(tuple, 1, PyString_FromStringAndSize((const char*)entry.text.data(), entry.text.size()));

        PyList_Append(ret, tuple);
        Py_DECREF(tuple); // the list owns a reference now
    }

    // We're left with one extra reference.
    Py_DECREF(opcodes[dmp.DELETE]);
    Py_DECREF(opcodes[dmp.INSERT]);
    Py_DECREF(opcodes[dmp.EQUAL]);
    
    return ret;
}

#if PY_MAJOR_VERSION == 2
static PyMethodDef MyMethods[] = {
    {"diff_unicode", (PyObject* (*)(PyObject*, PyObject*))diff_match_patch_diff<const wchar_t, 'u', std::wstring, Py_UNICODE>, METH_VARARGS|METH_KEYWORDS,
    "Compute the difference between two Unicode strings. Returns a list of tuples (OP, LEN)."},
    {"diff_str", (PyObject* (*)(PyObject*, PyObject*))diff_match_patch_diff<const char, 's', std::string, char*>, METH_VARARGS|METH_KEYWORDS,
    "Compute the difference between two (regular) strings. Returns a list of tuples (OP, LEN)."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initdiff_match_patch(void)
{
    (void) Py_InitModule("diff_match_patch", MyMethods);
}
#endif

#if PY_MAJOR_VERSION == 3
static PyMethodDef MyMethods[] = {
    {"diff", (PyObject* (*)(PyObject*, PyObject*))diff_match_patch_diff<const wchar_t, 'u', std::wstring, Py_UNICODE>, METH_VARARGS|METH_KEYWORDS,
    "Compute the difference between two strings. Returns a list of tuples (OP, LEN)."},
    {"diff_bytes", (PyObject* (*)(PyObject*, PyObject*))diff_match_patch_diff<const char, 'y', std::string, char*>, METH_VARARGS|METH_KEYWORDS,
    "Compute the difference between two byte strings. Returns a list of tuples (OP, LEN)."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef mymodule = {
   PyModuleDef_HEAD_INIT,
   "diff_match_patch",   /* name of module */
   NULL, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   MyMethods
};

PyMODINIT_FUNC
PyInit_diff_match_patch(void)
{
    return PyModule_Create(&mymodule);
}
#endif
