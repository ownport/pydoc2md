#!/usr/bin/env python

"""
pydoc2md.py
-----------
This module contains a simple class to output Markdown-style pydocs.

* Links:

- [Markdown syntax]<http://sourceforge.net/p/pydoc/wiki/markdown_syntax/>
"""

__author__ = 'Andrey Usov <https://github.com/ownport/pydoc2md>'
__version__ = '0.1'

import pydoc
import inspect

def render_doc(thing):
    """Render text documentation, given an object or a path to an object."""
    obj, name = pydoc.resolve(thing, forceload=0)
    desc = pydoc.describe(obj)
    module = inspect.getmodule(obj)
    if name and '.' in name:
        desc += ' in ' + name[:name.rfind('.')]
    elif module and module is not obj:
        desc += ' in module ' + module.__name__
    if type(obj) is pydoc._OLD_INSTANCE_TYPE:
        # If the passed object is an instance of an old-style class,
        # document its available methods instead of its value.
        obj = obj.__class__
    elif not (inspect.ismodule(obj) or
              inspect.isclass(obj) or
              inspect.isroutine(obj) or
              inspect.isgetsetdescriptor(obj) or
              inspect.ismemberdescriptor(obj) or
              isinstance(obj, property)):
        # If the passed object is a piece of data or an instance,
        # document its available methods instead of its value.
        obj = type(obj)
        desc += ' object'
    return '# %s' % desc + '\n\n' + str(txt2md.document(obj, name))

class TextDoc2Markdown(pydoc.TextDoc):

    def bold(self, text):
        """Format a string in bold by overstriking."""
        return "**%s**" % text

    def indent(self, text, prefix='    '):
        """Indent text by prepending a given prefix to each line."""
        if not text: return ''
        lines = text.split('\n')
        lines = map(lambda line, prefix=prefix: prefix + line, lines)
        if lines: lines[-1] = lines[-1].rstrip()
        return '\n'.join(lines)

    def section(self, title, contents):
        """Format a section with a given heading."""
        return self.bold(title) + '\n' + self.indent(contents).rstrip() + '\n\n'

        
txt2md = TextDoc2Markdown()

def cli():
    """Command-line interface (looks at sys.argv to decide what to do)."""

    import os
    import sys
    import getopt
    class BadUsage: pass

    # Scripts don't get the current directory in their path by default
    # unless they are run with the '-m' switch
    if '' not in sys.path:
        scriptdir = os.path.dirname(sys.argv[0])
        if scriptdir in sys.path:
            sys.path.remove(scriptdir)
        sys.path.insert(0, '.')
    
    try:
        if len(sys.argv) < 2:
            raise BadUsage
        for arg in sys.argv[1:]:
            if pydoc.ispath(arg) and not os.path.exists(arg):
                print 'file %r does not exist' % arg
                break
            try:
                print render_doc(arg)
            except (ImportError, pydoc.ErrorDuringImport), err:
                print err
    except BadUsage:
        cmd = os.path.basename(sys.argv[0])
        print """pydoc2md - the Python documentation tool in Markdown format

%s <name> ...
    Show documentation in Markdown formam.  <name> may be the name 
    of a Python function, module, or package, or a dotted reference 
    to a class or function within a module or module in a package.  
    If <name> contains a '%s', it is used as the path to a Python 
    source file to document.
""" % (cmd, os.sep)

if __name__ == '__main__':
    cli()    		
