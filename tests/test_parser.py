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
from __future__ import print_function

import sys, os, unittest, subprocess, argparse, ast, pprint, codecs

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'src'))
from parse import initialize_optimade_parser, parse_optimade_filter, ParserError

tests = os.path.abspath(os.path.dirname(__file__))
directory = os.path.join(tests,'parser_test_data','input')
directory_out = os.path.join(tests,'parser_test_data','output')

class TestParser(unittest.TestCase):
    pass

filter_input_pass = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(".filter") and not f.endswith("_fail.filter")]
filter_input_fail = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith("_fail.filter")]

def pass_function_factory(filter_input_file, filter_output_file):
    def exec_func(self):
        with open(os.path.join(directory,filter_input_file),'r') as f:
            filter_input = f.read()
        try:
            filter_ast = parse_optimade_filter(filter_input)
        except ParserError:
            self.assertFalse(True,msg="Filter string did not parse: "+str(filter_input))

        with codecs.open(os.path.join(directory,filter_output_file),'r',encoding='utf-8') as f:
            filter_expected_output_string = f.read()
        filter_expected_output = ast.literal_eval(filter_expected_output_string)
        self.assertTrue(filter_expected_output == filter_ast,msg="Parse tree does not match pre-recorded output.\n"+"==== Expected: ====\n"+filter_expected_output_string+"==== Got: ====\n"+pprint.pformat(filter_ast)+"\n====")
            
    return exec_func

def fail_function_factory(filter_input_file):
    def exec_func(self):
        with open(os.path.join(directory,filter_input_file),'r') as f:
            filter_input = f.read()
        try:
            filter_ast = parse_optimade_filter(filter_input)
        except ParserError:
            pass
        else:
            self.assertFalse(True,msg="Filter string meant to fail parsing unexpectedly passed: "+str(filter_input))
    return exec_func

for filter_input_file in filter_input_pass:
    filter_name, ext = os.path.splitext(filter_input_file)
    exec_func = pass_function_factory(filter_input_file, os.path.join(directory_out,filter_name+".out"))
    setattr(TestParser,'test_parse_filter_'+filter_name,exec_func)

for filter_input_file in filter_input_fail:
    exec_func = fail_function_factory(filter_input_file)
    filter_name, ext = os.path.splitext(filter_input_file)
    setattr(TestParser,'test_parse_filter_'+filter_name,exec_func)    

    
#############################################################################

            
if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == 'out':

        for filter_input_file in filter_input_pass:        
            filter_name, ext = os.path.splitext(filter_input_file)        
            outname = os.path.join(directory_out,filter_name+".out")
            if os.path.exists(outname):
                print("Skipping existing:"+filter_name)
                continue
            print("Generating:"+filter_name)
            with open(os.path.join(directory,filter_input_file),'r') as f:
                filter_input = f.read()
            filter_ast = parse_optimade_filter(filter_input)
            with codecs.open(outname, "w", encoding='utf-8') as fout:
                pprint.pprint(filter_ast, fout)
            
    else:    
        ap = argparse.ArgumentParser(description="Example tests")
        args, leftovers = ap.parse_known_args()
    
        suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
        unittest.TextTestRunner(verbosity=2).run(suite)        

    
