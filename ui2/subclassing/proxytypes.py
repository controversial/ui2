"""A modified copy of ProxyTypes 0.9 (https://pypi.io/project/ProxyTypes/)."""

"""
========== NOTICE OF MODIFICATION ==========

This version HAS BEEN MODIFIED from the original 'proxies.py' file, which was
published on July 20, 2006.

Modifications made on July 18, 2016:
  - Rewriting for compliance with the PEP 8 style guide
  - Supporting for Python 3
  - Movinging from the old format syntax (%) to the newer .format() syntax.
Modifications made on July 19, 2016:
  - Removing CallbackProxy, LazyProxy, CallbackWrapper, and LazyWrapper
  - Removing use of __slots__ because of conflicts
  - Renaming this file from proxies.py to proxytypes.py

Overall, these modifications serve as a clean-up and removal of classes I don't
need, rather than a change to the functionality or structure of the code that
remains after my removals.

=========== ORIGINAL AUTHORSHIP AND LICENSING ==========

ProxyTypes was originally written by Phillip J. Eby, and published under the
Zope Public License (ZPL). This modified version is published under the MIT
license, available in the LICENSE.md file at the root of this repository.

The ZPL is as follows:

Zope Public License (ZPL) Version 2.0
-----------------------------------------------

This software is Copyright (c) Zope Corporation (tm) and
Contributors. All rights reserved.

This license has been certified as open source. It has also
been designated as GPL compatible by the Free Software
Foundation (FSF).

Redistribution and use in source and binary forms, with or
without modification, are permitted provided that the
following conditions are met:

1. Redistributions in source code must retain the above
   copyright notice, this list of conditions, and the following
   disclaimer.

2. Redistributions in binary form must reproduce the above
   copyright notice, this list of conditions, and the following
   disclaimer in the documentation and/or other materials
   provided with the distribution.

3. The name Zope Corporation (tm) must not be used to
   endorse or promote products derived from this software
   without prior written permission from Zope Corporation.

4. The right to distribute this software or to use it for
   any purpose does not give you the right to use Servicemarks
   (sm) or Trademarks (tm) of Zope Corporation. Use of them is
   covered in a separate agreement (see
   http://www.zope.com/Marks).

5. If any files are modified, you must cause the modified
   files to carry prominent notices stating that you changed
   the files and the date of any change.

Disclaimer

  THIS SOFTWARE IS PROVIDED BY ZOPE CORPORATION ``AS IS''
  AND ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT
  NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
  AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN
  NO EVENT SHALL ZOPE CORPORATION OR ITS CONTRIBUTORS BE
  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
  OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
  DAMAGE.


This software consists of contributions made by Zope
Corporation and many individuals on behalf of Zope
Corporation.  Specific attributions are listed in the
accompanying credits file.
"""


class AbstractProxy(object):
    """Delegates all operations (except ``.__subject__``) to another object."""

    # Delegate getting, setting, and deleting attributes

    def __getattribute__(self, attr, oga=object.__getattribute__):
        subject = oga(self, "__subject__")
        if attr == "__subject__":
            return subject
        return getattr(subject, attr)

    def __setattr__(self, attr, val, osa=object.__setattr__):
        if attr == "__subject__":
            osa(self, attr, val)
        else:
            setattr(self.__subject__, attr, val)

    def __delattr__(self, attr, oda=object.__delattr__):
        if attr == "__subject__":
            oda(self, attr)
        else:
            delattr(self.__subject__, attr)

    # Delegate the getting, setting, and deleting of items with []

    def __getitem__(self, arg):
        return self.__subject__[arg]

    def __setitem__(self, arg, val):
        self.__subject__[arg] = val

    def __delitem__(self, arg):
        del self.__subject__[arg]

    # Delegate the getting, setting, and deleting of slices with []

    def __getslice__(self, i, j):
        return self.__subject__[i:j]

    def __setslice__(self, i, j, val):
        self.__subject__[i:j] = val

    def __delslice__(self, i, j):
        del self.__subject__[i:j]

    # Delegate calling

    def __call__(self, *args, **kwargs):
        return self.__subject__(*args, **kwargs)

    # Delegate true/false testing

    def __nonzero__(self):
        return bool(self.__subject__)

    # Delegate the 'in' operator

    def __contains__(self, ob):
        return ob in self.__subject__

    # Delegate magic methods with no arguments

    for name in ("repr", "str", "hash", "len", "abs", "complex", "int", "long",
                 "float", "iter", "oct", "hex"):
        exec(("def __{}__(self):"
              "    return {}(self.__subject__)").format(name, name))

    for name in "cmp", "coerce", "divmod":
        exec(("def __{}__(self, ob):"
              "    return {}(self.__subject__, ob)").format(name, name))

    # Delegate comparison operators

    for name, operator in [
        ("lt", "<"), ("gt", ">"), ("le", "<="), ("ge", ">="),
        ("eq", "=="), ("ne", "!=")
    ]:
        exec(("def __{}__(self, ob):"
              "    return self.__subject__ {} ob").format(name, operator))

    # Delegate unary operators

    for name, op in [("neg", "-"), ("pos", "+"), ("invert", "~")]:
        exec(("def __{}__(self):"
              "    return {} self.__subject__").format(name, op))

    # Delegate arithmetic, bitwise, and shift operators

    for name, op in [
        ("or", "|"), ("and", "&"), ("xor", "^"),  # Bitwise operators
        ("lshift", "<<"), ("rshift", ">>"),  # Shift operators
        ("add", "+"), ("sub", "-"), ("mul", "*"), ("div", "/"),  # Arithmetic
        ("mod", "%"), ("truediv", "/"), ("floordiv", "//")  # Weird arithmetic
    ]:
        exec("\n".join([
            "def __{0}__(self, ob):",
            "    return self.__subject__ {1} ob",

            "def __r{0}__(self, ob):",
            "    return ob {1} self.__subject__",

            "def __i{0}__(self, ob):",
            "    self.__subject__ {1}= ob",
            "    return self"
        ]).format(name, op))

    del name, op

    # Oddball signatures

    def __rdivmod__(self, ob):
        return divmod(ob, self.__subject__)

    def __pow__(self, *args):
        return pow(self.__subject__, *args)

    def __ipow__(self, ob):
        self.__subject__ **= ob
        return self

    def __rpow__(self, ob):
        return pow(ob, self.__subject__)


class ObjectProxy(AbstractProxy):
    """Proxy for a specific object."""

    def __init__(self, subject):
        self.__subject__ = subject


class AbstractWrapper(AbstractProxy):
    """Mixin to allow extra behaviors and attributes on proxy instance."""
    def __getattribute__(self, attr, oga=object.__getattribute__):
        if attr.startswith("__"):
            subject = oga(self, "__subject__")
            if attr == "__subject__":
                return subject
            return getattr(subject, attr)
        return oga(self, attr)

    def __getattr__(self, attr, oga=object.__getattribute__):
        return getattr(oga(self, "__subject__"), attr)

    def __setattr__(self, attr, val, osa=object.__setattr__):
        if (
            attr == "__subject__" or
            hasattr(type(self), attr) and not
            attr.startswith("__")
        ):
            osa(self, attr, val)
        else:
            setattr(self.__subject__, attr, val)

    def __delattr__(self, attr, oda=object.__delattr__):
        if (
            attr == "__subject__" or
            hasattr(type(self), attr) and not attr.startswith("__")
        ):
            oda(self, attr)
        else:
            delattr(self.__subject__, attr)


class ObjectWrapper(ObjectProxy, AbstractWrapper):
    pass
