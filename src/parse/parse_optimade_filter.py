#!/usr/bin/env python
#
# Copyright 2019 Rickard Armiento
#
# This file is part of a Python candidate reference implementation of
# the optimade API [https://www.optimade.org/]
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os, re
from pprint import pprint

from . miniparser import parser, build_ls, LogVerbosity

ls = None


def parse_optimade_filter(filter_string, verbosity=0):
    # To get diagnostic output, pass argument, e.g.,: verbosity=LogVerbosity(0,parser_verbosity=5))

    parse_tree = parse_optimade_filter_raw(filter_string, verbosity=verbosity)
    ast = simplify_optimade_filter_ast(parse_tree)
    return ast


def parse_optimade_filter_raw(filter_string, verbosity=0):
    global ls

    if ls is None:
        initialize_optimade_parser(spaces_hack=True)

    return parser(ls, filter_string, verbosity=verbosity)


def initialize_optimade_parser(spaces_hack=True):

    global ls

    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, "optimade_filter_grammar.ebnf")) as f:
        grammar = f.read()

    # We need to replace the PCRE to a Python-compatible form.
    grammar = grammar.replace(r"UnicodeHighChar = ? [^\p{ASCII}] ? ;", "UnicodeHighChar = ? [^\x00-\xFF] ? ;")

    if spaces_hack:
        # Remove the space handling, we do that in the tokenizer
        # This greatly simplifies parsing, and seems to remove
        # a shift/reduce ambiguity in the grammar
        grammar = grammar.replace("Space = ' ' | '\t' ;", "")
        grammar = grammar.replace("Spaces = Space, { Space } ;", "")
        grammar = re.sub(r"(\[ *Spaces *\] *,)|(, *\[ *Spaces *\])", "", grammar)

    # Keywords
    literals = ["filter=", "AND", "NOT", "OR", ")", "("]

    # Token definitions from Appendix 3 (they are not all there yet)
    tokens = {
        "Operator": r'<|<=|>|>=|=|!=',
        "Identifier": "[a-zA-Z_][a-zA-Z_0-9]*",
        "String": r'"[^"\\]*(?:\\.[^"\\]*)*"',
        "Number": r"[-+]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][-+]?[0-9]+)?",
    }
    # We don't need these, because they are handled on higher level
    # by the token definitions.
    skip = [
        "EscapedChar", "UnescapedChar", "Punctuator", "Exponent", "Sign",
        "Digits", "Digit", "Letter", "Space"
    ]

    ls = build_ls(ebnf_grammar=grammar, start='Filter', ignore=' \t\n',
                  tokens=tokens, literals=literals, verbosity=0, skip=skip,
                  remove=['Spaces', ')', '('], simplify=[])  # , simplify=['Term', 'Atom', 'Expression'])

    return ls


def simplify_optimade_filter_ast(ast):

    assert(ast[0] == 'Filter')
    assert(ast[1][0] == 'Keyword' and ast[1][1][0] == 'filter=')
    return simplify_optimade_filter_ast_recurse(ast[2])


def simplify_optimade_filter_ast_recurse(node, recursion=0):
    indent = recursion*"  "

    tree = [None]
    pos = tree
    arg = 0

    if node[0] in ['Expression', 'Term', 'Atom', 'AndComparison']:            
        n = node[1:]
        if n[0][0] == "NOT":
            assert(arg is not None)
            pos[arg] = ['NOT', None]
            pos = pos[arg]
            arg = 1
            n = list(n)[1:]
        for nn in n:
            if nn[0] in ['Expression', 'Term', 'Atom', 'Comparison', 'AndComparison']:
                assert(arg is not None and pos[arg] is None)
                pos[arg] = simplify_optimade_filter_ast_recurse(nn, recursion=recursion+1)
            elif nn[0] in ["AND", "OR"]:
                assert(arg is not None and pos[arg] is not None)
                pos[arg] = [nn[0], tuple(pos[arg]), None]
                pos = pos[arg]
                arg = 2
            else:
                pprint(nn)
                raise Exception("Translation error:"+str(nn[0]))
    elif node[0] == 'Comparison':        
        assert(arg is not None and pos[arg] is None)
        assert(node[1][0] == 'Value')
        assert(node[2][0] == 'Operator')
        op = node[2][1]
        assert(node[3][0] == 'Value')
        left = node[1][1] 
        right = node[3][1]
        pos[arg] = (op, left, right)
        arg = None
    else:
        pprint(node)
        raise Exception("Translation error")

    assert(arg is None or pos[arg] is not None)
    return tuple(tree[0])

