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

from .miniparser import parser, build_ls, ParserError

ls = None


def parse_optimade_filter(filter_string, verbosity=0):
    # To get diagnostic output, pass argument, e.g.,: verbosity=LogVerbosity(0,parser_verbosity=5))

    parse_tree = parse_optimade_filter_raw(filter_string, verbosity)

    ast = simplify_optimade_filter_ast(parse_tree)
    return ast


def parse_optimade_filter_raw(filter_string, verbosity=0):
    global ls

    if ls is None:
        initialize_optimade_parser()

    return parser(ls, filter_string, verbosity=verbosity)


def initialize_optimade_parser():

    global ls

    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, "optimade_filter_grammar.ebnf")) as f:
        grammar = f.read()

    # Keywords
    literals = ["AND", "NOT", "OR", "KNOWN", "UNKNOWN", "IS", "CONTAINS", "STARTS", "ENDS", "LENGTH", "HAS", "ALL", "ONLY", "EXACTLY", "ANY", ")", "(", ":", ","," ","\t","\n","\r"]

    # Token definitions from Appendix 3 (they are not all there yet)
    tokens = {
        "Operator": r'<|<=|>|>=|=|!=',
        "Identifier": "[a-zA-Z_][a-zA-Z_0-9]*",
        "String": r'"[^"\\]*(?:\\.[^"\\]*)*"',
        "Number": r"[-+]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][-+]?[0-9]+)?"
    }
    partial_tokens = {
        "Number": r"[-+]?[0-9]*\.?[0-9]*[eE]?[-+]?[0-9]*"
    }
    # We don't need these, because they are handled on higher level
    # by the token definitions.
    skip = [
        "EscapedChar", "UnescapedChar", "Punctuator", "Exponent", "Sign",
        "Digits", "Digit", "Letter", "Operator"
    ]

    ls = build_ls(ebnf_grammar=grammar, start='Filter', ignore=' \t\n',
                  tokens=tokens, partial_tokens=partial_tokens, literals=literals, verbosity=0, skip=skip,
                  remove=[')', '('], simplify=[])  # , simplify=['Term', 'Atom', 'Expression'])

    return ls


def simplify_optimade_filter_ast(ast):

    assert(ast[0] == 'Filter')
    return simplify_optimade_filter_ast_recurse(ast[1])


def simplify_optimade_filter_ast_recurse(node, recursion=0):

    tree = [None]
    pos = tree
    arg = 0

    if node[0] in ['Expression', 'ExpressionClause', 'ExpressionPhrase']:
        n = node[1:]
        if n[0][0] == "NOT":
            assert(arg is not None)
            pos[arg] = ['NOT', None]
            pos = pos[arg]
            arg = 1
            n = list(n)[1:]
        for nn in n:
            if nn[0] in ['Expression', 'ExpressionClause', 'ExpressionPhrase', 'Comparison', 'PredicateComparison']:
                assert(arg is not None and pos[arg] is None)
                pos[arg] = simplify_optimade_filter_ast_recurse(nn, recursion=recursion+1)
            elif nn[0] in ["AND", "OR"]:
                assert(arg is not None and pos[arg] is not None)
                pos[arg] = [nn[0], tuple(pos[arg]), None]
                pos = pos[arg]
                arg = 2
            else:
                pprint(nn)
                raise Exception("Internal error: filter simplify on invalid ast: "+str(nn[0]))
    elif node[0] == 'Comparison':        
        assert(arg is not None and pos[arg] is None)
        assert(node[1][0] == 'Identifier')

        if node[2][0] == "ValueOpRhs":            
            assert(node[2][1][0] == 'Operator')
            op = node[2][1][1]
            assert(node[2][2][0] == 'Value')
            left = node[1] 
            right = node[2][2][1]
            pos[arg] = (op, left, right)
            arg = None
        elif node[2][0] == "FuzzyStringOpRhs":            
            assert(node[2][1][0] in ['CONTAINS', 'STARTS', 'ENDS'])
            op = node[2][1][1]
            assert(node[2][2][0] == 'String')
            left = node[1] 
            right = node[2][2]
            pos[arg] = (op, left, right)
            arg = None
        elif node[2][0] == "KnownOpRhs":            
            assert(node[2][1][0] == 'IS')
            op = node[2][1][1]
            assert(node[2][2][0] in ['KNOWN','UNKNOWN'])
            op += "_" + node[2][2][0] 
            operand = node[1] 
            pos[arg] = (op, operand)
            arg = None            
        elif node[2][0] == "SetOpRhs":
            assert(node[2][1][0] == 'HAS')
            left = node[1] 
            if len(node[2]) == 3:
                op = "HAS"
                assert(node[2][2][0] == 'Value')
                right = node[2][2][1]
            elif len(node[2]) == 4:            
                assert(node[2][2][0] in ['ONLY', 'ALL', 'EXACTLY', 'ANY'])
                op = "HAS_"+node[2][2][0]
                assert(node[2][3][0] == 'ValueList')
                right = tuple(x[1] for x in node[2][3][1::2])
            else:
                raise Exception("Internal error: filter simplify on invalid ast, unexpected number of components in set op: "+str(node[2]))
            pos[arg] = (op, left, right)
            arg = None
        elif node[2][0] == "SetZipOpRhs":
            assert(node[2][1][0] == 'IdentifierZipAddon')
            left = (node[1],) + node[2][1][2::2] 
            nzip = len(left)
            assert(node[2][2][0] == 'HAS')
            if len(node[2]) == 4:
                op = "HAS_ZIP"
                assert(node[2][3][0] == 'ValueZip')
                assert(node[2][3][1][0] == 'Value')
                right = node[2][3][1][1]
                if not nzip==len(right):
                    raise ParserError("Parser context error: set zip operation with mismatching number of components for:"+str(right)+" lhs:"+str(nzip)+" rhs:"+str(right))
            elif len(node[2]) == 5:            
                assert(node[2][3][0] in ['ONLY', 'ALL', 'EXACTLY', 'ANY'])
                op = "HAS_ZIP_"+node[2][3][0]
                assert(node[2][4][0] == 'ValueZipList')
                right = tuple(tuple(y[1] for y in x[1::2]) for x in node[2][4][1::2])
                if not all(nzip==len(x) for x in right):
                    raise ParserError("Parser context error: set zip operation with mismatching number of components for:"+str(right)+" lhs:"+str(nzip)+" rhs:"+str([len(x) for x in right]))                
            else:
                raise Exception("Internal error: filter simplify on invalid ast, unexpected number of components in set zip op: "+str(node[2]))
            pos[arg] = (op, left, right)
            arg = None
        else:
            raise Exception("Internal error: filter simplify on invalid ast, unrecognized comparison: "+str(node[2][0]))
    elif node[0] == 'PredicateComparison':
        if node[1][0] == "LengthComparison":
            assert(node[1][1][0]=="LENGTH")
            assert(node[1][2][0]=="Identifier")
            assert(node[1][3][0]=="Operator")
            assert(node[1][4][0]=="Value")
            left = node[1][2]
            right = node[1][4][1]
            op = node[1][3][1]
            pos[arg] = ("LENGTH", op, left, right)
            arg = None
        else:
            raise Exception("Internal error: filter simplify on invalid ast, unrecognized predicate comparison: "+str(node[1][0]))
    else:
        raise Exception("Internal error: filter simplify on invalid ast, unrecognized node: "+str(node[0]))

    assert(arg is None or pos[arg] is not None)
    return tuple(tree[0])

