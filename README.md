# module pydoc2md

## Name

pydoc2md - pydoc2md.py

## Description

Simple script for creation python code documentation in Markdown format

### how to use

```shell
$ ./pydoc2md pydoc2md > README.md
```

### links

- [Markdown syntax](http://sourceforge.net/p/pydoc/wiki/markdown_syntax/)

## Classes Tree

```text
+-- __builtin__.object
|  +-- TextDoc2Markdown(pydoc.TextDoc, __builtin__.object)
+-- pydoc.TextDoc(pydoc.Doc)
|  +-- TextDoc2Markdown(pydoc.TextDoc, __builtin__.object)
```

## Classes

### class **TextDoc2Markdown**(pydoc.TextDoc, __builtin__.object)
PyDoc in Markdown format

#### bold(self, text)
*Format a string in bold*


#### docclass(self, object, name=None, mod=None)
*Produce text documentation for a given class object.*


#### docdata(self, object, name=None, mod=None, cl=None)
*Produce text documentation for a data descriptor.*


#### docmodule(self, object, name=None, mod=None)
*Produce text documentation for a given module object.*


#### docother(self, object, name=None, mod=None, parent=None, maxlen=None, doc=None)
*Produce text documentation for a data object.*


#### docproperty(self, object, name=None, mod=None, cl=None)
*Produce text documentation for a property.*


#### docroutine(self, object, name=None, mod=None, cl=None)
*Produce text documentation for a function or method object.*


#### document(self, object, name=None, *args)
*Generate documentation for an object.*


#### fail(self, object, name=None, *args)
*Raise an exception for unimplemented types.*


#### formattree(self, tree, modname, parent=None, prefix='+-- ')
*Render in text a class tree as returned by inspect.getclasstree().*


#### formatvalue(self, object)
*Format an argument default value as text.*


#### getdocloc(self, object)
*Return the location of module docs or None*


#### indent(self, text, prefix='')
*Indent text by prepending a given prefix to each line.*


#### repr(self, x) from pydoc.TextRepr

#### section(self, title, contents)
*Format a section with a given heading.*

## Functions

#### cli()
*Command-line interface (looks at sys.argv to decide what to do).*

## Data

**__all__** = ['render_doc', 'TextDoc2Markdown']
**__author__** = 'Andrey Usov <https://github.com/ownport/pydoc2md>'
**__file__** = './pydoc2md.pyc'
**__name__** = 'pydoc2md'
**__package__** = None
**__version__** = '0.1'

## Version

0.1

## Author

Andrey Usov <https://github.com/ownport/pydoc2md>


