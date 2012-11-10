# module pydoc2md

**NAME**
    pydoc2md

**FILE**
    /media/data/devel/git-repos/pydoc2md/pydoc2md.py

**DESCRIPTION**
    pydoc2md.py
    -----------
    This module contains a simple class to output Markdown-style pydocs.
    
    * Links:
    
    - [Markdown syntax]<http://sourceforge.net/p/pydoc/wiki/markdown_syntax/>

**CLASSES**
    pydoc.TextDoc(pydoc.Doc)
        TextDoc2Markdown
    
    class **TextDoc2Markdown**(pydoc.TextDoc)
     |  Method resolution order:
     |      TextDoc2Markdown
     |      pydoc.TextDoc
     |      pydoc.Doc
     |  
     |  Methods defined here:
     |  
     |  **bold**(self, text)
     |      Format a string in bold by overstriking.
     |  
     |  **indent**(self, text, prefix='    ')
     |      Indent text by prepending a given prefix to each line.
     |  
     |  **section**(self, title, contents)
     |      Format a section with a given heading.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from pydoc.TextDoc:
     |  
     |  **docclass**(self, object, name=None, mod=None, *ignored)
     |      Produce text documentation for a given class object.
     |  
     |  **docdata**(self, object, name=None, mod=None, cl=None)
     |      Produce text documentation for a data descriptor.
     |  
     |  **docmodule**(self, object, name=None, mod=None)
     |      Produce text documentation for a given module object.
     |  
     |  **docother**(self, object, name=None, mod=None, parent=None, maxlen=None, doc=None)
     |      Produce text documentation for a data object.
     |  
     |  **docproperty**(self, object, name=None, mod=None, cl=None)
     |      Produce text documentation for a property.
     |  
     |  **docroutine**(self, object, name=None, mod=None, cl=None)
     |      Produce text documentation for a function or method object.
     |  
     |  **formattree**(self, tree, modname, parent=None, prefix='')
     |      Render in text a class tree as returned by inspect.getclasstree().
     |  
     |  **formatvalue**(self, object)
     |      Format an argument default value as text.
     |  
     |  **repr**(self, x) from pydoc.TextRepr
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from pydoc.Doc:
     |  
     |  **document**(self, object, name=None, *args)
     |      Generate documentation for an object.
     |  
     |  **fail**(self, object, name=None, *args)
     |      Raise an exception for unimplemented types.
     |  
     |  **getdocloc**(self, object)
     |      Return the location of module docs or None

**FUNCTIONS**
    **cli**()
        Command-line interface (looks at sys.argv to decide what to do).
    
    **render_doc**(thing)
        Render text documentation, given an object or a path to an object.

**DATA**
    **__author__** = 'Andrey Usov <https://github.com/ownport/pydoc2md>'
    **__version__** = '0.1'
    **txt2md** = <pydoc2md.TextDoc2Markdown instance>

**VERSION**
    0.1

**AUTHOR**
    Andrey Usov <https://github.com/ownport/pydoc2md>


