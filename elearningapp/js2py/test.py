__all__ = ['test']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers([])
var.get('console').callprop('log', Js('a'))
pass


# Add lib to the module scope
test = var.to_python()