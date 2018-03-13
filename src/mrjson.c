
#include "py_defines.h"

#define STRINGIFY(x) XSTRINGIFY(x)
#define XSTRINGIFY(x) #x

PyObject* toJson    (PyObject* self, PyObject *args, PyObject *kwargs);
PyObject* toJsonFile(PyObject* self, PyObject *args, PyObject *kwargs);

PyObject* fromJson    (PyObject* self, PyObject *args, PyObject *kwargs);
PyObject* fromJsonFile(PyObject* self, PyObject *args, PyObject *kwargs);


PyDoc_STRVAR(docstring,
             "loads(string, *, ensure_ascii=False)\n"
             "\n"
             "Decode a JSON string into a Python object.");

static PyMethodDef mrjsonMethods[] = {
  {"encode", (PyCFunction) toJson,       METH_VARARGS | METH_KEYWORDS, docstring },
  {"decode", (PyCFunction) fromJson,     METH_VARARGS | METH_KEYWORDS, docstring },
  {"dumps",  (PyCFunction) toJson,       METH_VARARGS | METH_KEYWORDS, docstring },
  {"loads",  (PyCFunction) fromJson,     METH_VARARGS | METH_KEYWORDS, docstring },
  {"dump",   (PyCFunction) toJsonFile,   METH_VARARGS | METH_KEYWORDS, docstring },
  {"load",   (PyCFunction) fromJsonFile, METH_VARARGS | METH_KEYWORDS, docstring },
  {NULL, NULL, 0, NULL}       /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT,
  "mrjson",
  0,              /* m_doc */
  -1,             /* m_size */
  mrjsonMethods,   /* m_methods */
  NULL,           /* m_reload */
  NULL,           /* m_traverse */
  NULL,           /* m_clear */
  NULL            /* m_free */
};

#define PYMODINITFUNC       PyObject *PyInit_mrjson(void)
#define PYMODULE_CREATE()   PyModule_Create(&moduledef)
#define MODINITERROR        return NULL

#else

#define PYMODINITFUNC       PyMODINIT_FUNC initmrjson(void)
#define PYMODULE_CREATE()   Py_InitModule("mrjson", mrjsonMethods)
#define MODINITERROR        return

#endif

PYMODINITFUNC
{
  PyObject *m;
  PyObject *v;

  //initObjToJSON();
  m = PYMODULE_CREATE();

  if (m == NULL) { MODINITERROR; }

  PyModule_AddStringConstant(m, "__version__", STRINGIFY(MRJSON_VERSION));
  PyModule_AddStringConstant(m, "__author__", "Mark Reed <mark@untilfluent.com>");
#if PY_MAJOR_VERSION >= 3
  return m;
#endif
}
