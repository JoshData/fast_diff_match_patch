#include <Python.h>
#include <QtCore>

#include "diff_match_patch.h"

static PyObject *
diff_match_patch_diff(PyObject *self, PyObject *args)
{
    const char *a, *b;

    if (!PyArg_ParseTuple(args, "ss", &a, &b))
        return NULL;
    
    PyObject *ret = PyList_New(0);
    
    PyObject *opcodes[3];
    opcodes[DELETE] = PyString_FromString("-");
    opcodes[INSERT] = PyString_FromString("+");
    opcodes[EQUAL] = PyString_FromString("=");
    
    diff_match_patch dmp = diff_match_patch();
    QList<Diff> diff = dmp.diff_main(QString(a), QString(b));
    foreach(Diff entry, diff) {
		PyObject* tuple = PyTuple_New(2);
		PyTuple_SetItem(tuple, 0, opcodes[entry.operation]);
		PyTuple_SetItem(tuple, 1, PyInt_FromLong(entry.text.length()));
    	PyList_Append(ret, tuple);
    }
    
    return ret;
}

static PyMethodDef SpamMethods[] = {
    {"diff", diff_match_patch_diff, METH_VARARGS,
    "Compute the difference between two strings. Returns a list of tuples (OP, LEN)."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initdiff_match_patch(void)
{
    (void) Py_InitModule("diff_match_patch", SpamMethods);
}

