#!/usr/bin/env python
#   -*- coding: utf-8 -*-
'''
pydoc2md.py

Simple script for creation python code documentation in Markdown format

### how to use

```shell
$ ./pydoc2md pydoc2md > README.md
```

### links

- [Markdown syntax](http://sourceforge.net/p/pydoc/wiki/markdown_syntax/)

'''

__author__ = 'Andrey Usov <https://github.com/ownport/pydoc2md>'
__version__ = '0.1'

import os
import sys
import pydoc
import inspect
import __builtin__

__all__ = ['render_doc', 'TextDoc2Markdown',]


class TextDoc2Markdown(pydoc.TextDoc, object):
    ''' PyDoc in Markdown format

    '''

    # ------------------------------------------- text formatting utilities
    
    def indent(self, text, prefix=''):
        '''Indent text by prepending a given prefix to each line.
        '''
        return super(TextDoc2Markdown, self).indent(text, prefix=prefix)


    def bold(self, text):
        ''' Format a string in bold
        '''
        return "**%s**" % text


    def section(self, title, contents):
        ''' Format a section with a given heading.
        '''
        return '## %s' % title + '\n\n' + self.indent(contents).rstrip() + '\n\n'

    # ---------------------------------------------- type-specific routines

    def formattree(self, tree, modname, parent=None, prefix='+-- '):
        ''' Render in text a class tree as returned by inspect.getclasstree().
        '''
        result = []
        for entry in tree:
            if type(entry) is type(()):
                c, bases = entry
                entry_details = '%s%s' % (prefix, pydoc.classname(c, modname))
                if bases and bases != (parent,):
                    parents = map(lambda c, m=modname: pydoc.classname(c, m), bases)
                    entry_details += '(%s)' % ', '.join(parents)
                result.append(entry_details)
            elif type(entry) is type([]):
                result.append(self.formattree(entry, modname, c, '|  +-- '))
        return '\n'.join(result)


    def docmodule(self, object, name=None, mod=None):
        ''' Produce text documentation for a given module object.
        '''
        name = object.__name__ # ignore the passed-in name
        synop, desc = pydoc.splitdoc(pydoc.getdoc(object))
        result = self.section('Name', name + (synop and ' - ' + synop))
        if desc:
            result = result + self.section('Description', desc)

        classes = []
        for key, value in inspect.getmembers(object, inspect.isclass):
            if (inspect.getmodule(value) or object) is object:
                classes.append((key, value))
        funcs = []
        for key, value in inspect.getmembers(object, inspect.isroutine):
            if inspect.isbuiltin(value) or inspect.getmodule(value) is object:
                funcs.append((key, value))

        if hasattr(object, '__path__'):
            modpkgs = []
            for file in os.listdir(object.__path__[0]):
                path = os.path.join(object.__path__[0], file)
                modname = inspect.getmodulename(file)
                if modname and modname not in modpkgs:
                    modpkgs.append(modname)
                elif pydoc.ispackage(path):
                    modpkgs.append(file + ' (package)')
            modpkgs.sort()
            result = result + self.section(
                'Package contents', join(modpkgs, '\n'))

        if classes:
            classlist = map(lambda (key, value): value, classes)
            classes_tree = self.formattree(inspect.getclasstree(classlist, 1), name) 
            if classes_tree:
                classes_tree = '```text\n%s\n```\n' % classes_tree
                result = result + self.section('Classes Tree', classes_tree)

            contents = []
            for key, value in classes:
                contents.append(self.document(value, key, name))
            result = result + self.section('Classes', '\n'.join(contents))

        if funcs:
            contents = []
            for key, value in funcs:
                contents.append(self.document(value, key, name))
            result = result + self.section('Functions', '\n'.join(contents))

        if hasattr(object, '__version__'):
            version = str(object.__version__)
            if version[:11] == '$' + 'Revision: ' and version[-1:] == '$':
                version = strip(version[11:-1])
            result = result + self.section('Version', version)
        if hasattr(object, '__date__'):
            result = result + self.section('Date', str(object.__date__))
        if hasattr(object, '__author__'):
            result = result + self.section('Author', str(object.__author__))
        if hasattr(object, '__credits__'):
            result = result + self.section('Credits', str(object.__credits__))
        return result


    def docclass(self, object, name=None, mod=None):
        ''' Produce text documentation for a given class object.
        '''
        realname = object.__name__
        name = name or realname
        bases = object.__bases__

        if name == realname:
            title = '### class ' + self.bold(realname)
        else:
            title = '### ' + self.bold(name) + ' = class ' + realname
        if bases:
            def makename(c, m=object.__module__): return pydoc.classname(c, m)
            parents = map(makename, bases)
            title = title + '(%s)' % ', '.join(parents)

        doc = pydoc.getdoc(object)
        contents = doc and doc + '\n'
        methods = pydoc.allmethods(object).items()
        methods.sort()
        for key, value in methods:
            if key.startswith('_'):
                continue    
            contents = contents + '\n' + self.document(value, key, mod, object)

        if not contents: return title + '\n'
        return title + '\n' + self.indent(contents.rstrip()) + '\n'


    def docroutine(self, object, name=None, mod=None, cl=None):
        ''' Produce text documentation for a function or method object.
        '''
        realname = object.__name__
        name = name or realname
        note = ''
        skipdocs = 0
        if inspect.ismethod(object):
            imclass = object.im_class
            if cl:
                if imclass is not cl:
                    note = ' from ' + pydoc.classname(imclass, mod)
                    skipdocs = 1
            else:
                if object.im_self:
                    note = ' method of %s instance' % classname(
                        object.im_self.__class__, mod)
                else:
                    note = ' unbound %s method' % classname(imclass,mod)
            object = object.im_func

        if name == realname:
            # title = self.bold(realname)
            title = '#### ' + realname
        else:
            if (cl and cl.__dict__.has_key(realname) and
                cl.__dict__[realname] is object):
                skipdocs = 1
            # title = self.bold(name) + ' = ' + realname
            title = '####' + name + ' = ' + realname
        if inspect.isbuiltin(object):
            argspec = '(...)'
        else:
            args, varargs, varkw, defaults = inspect.getargspec(object)
            argspec = inspect.formatargspec(
                args, varargs, varkw, defaults, formatvalue=self.formatvalue)
            if realname == '<lambda>':
                title = 'lambda'
                argspec = argspec[1:-1] # remove parentheses
        decl = title + argspec + note

        if skipdocs:
            return decl + '\n'
        else:
            doc = pydoc.getdoc(object) or ''
            return decl + '\n' + '*%s*\n\n' % (doc and self.indent(doc).rstrip())



pydoc.text = TextDoc2Markdown()

def cli():
    ''' Command-line interface (looks at sys.argv to decide what to do).
    '''

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
                print pydoc.render_doc(arg, title='# %s')
            except (ImportError, pydoc.ErrorDuringImport), err:
                print err
    except BadUsage:
        cmd = os.path.basename(sys.argv[0])
        print '''pydoc2md - the Python documentation tool in Markdown format

%s <name> ...
    Show documentation in Markdown formam.  <name> may be the name 
    of a Python function, module, or package, or a dotted reference 
    to a class or function within a module or module in a package.  
    If <name> contains a '%s', it is used as the path to a Python 
    source file to document.
''' % (cmd, os.sep)

if __name__ == '__main__':
    cli()    		
