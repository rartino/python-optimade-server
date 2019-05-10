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

import os, sys, unittest, subprocess, argparse, time, signal, select, codecs

# Set this to True to show server stdout while running tests
show_output = False

top = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.join(top,'src'))

import validation

class TestServeExampleMongoDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.proc = subprocess.Popen(['stdbuf', '-o0'] + [os.path.join(top,'start_serve_example_mongodb.py')], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)        
        cls.o = select.poll()
        cls.o.register(cls.proc.stdout, select.POLLIN)
        cls.e = select.poll()
        cls.e.register(cls.proc.stderr, select.POLLIN)
        time.sleep(0.5)
        
    @classmethod
    def tearDownClass(cls):
        os.killpg(os.getpgid(cls.proc.pid), signal.SIGTERM)
        time.sleep(0.2)
        timeout = 5
        while cls.proc.poll() is None and timeout > 0:
            time.sleep(1.0)
            timeout -= 1
        if cls.proc.poll() is None:
            task.kill()            
        (out, err) = cls.proc.communicate()
        retcode = cls.proc.returncode
        # This is a bit hackish to be able to assert inside the class teardown, but it works
        tear_down_unittest = unittest.TestCase('__init__')
        tear_down_unittest.assertTrue(len(err.strip())==0, msg="Server produced output on stderr: "+(codecs.decode(err,'utf-8') if err is not None else ""))
        tear_down_unittest.assertTrue(retcode == 0 or retcode < 0, msg="Server exited with unexpected return code: "+str(retcode))

def function_factory(f):
    def exec_func(self):
        ret = f['test']('http://localhost:8080',f['relurl'])

        self.assertTrue(len(ret['error'])==0, msg="Validation errors:"+str(ret))

        time.sleep(0.2)
        out = None
        while True:
            received = False
            while self.o.poll(1):
                # This is required to preserve the type that comes out of stdout.read(1)
                # for python 2 and 3 compability.
                if out is None:
                    out = self.proc.stdout.read(1)
                else:
                    out += self.proc.stdout.read(1)
                received = True
            if not received:
                break
            time.sleep(0.2)
            
        err = None
        while True:
            received = False
            while self.e.poll(1): 
                if err is None:
                    err = self.proc.stdout.read(1)
                else:
                    err += self.proc.stdout.read(1)
                received = True
            if not received:
                break
            time.sleep(0.2)
            
        self.assertTrue(err is None or len(err.strip())==0, msg="Server produced output on stderr: "+(codecs.decode(err,'utf-8') if err is not None else ""))
        if show_output:
            print("\n################\n")
            print(out)
            print("\n################\n")
    return exec_func

for test in validation.all_tests:
    exec_func = function_factory(test)
    setattr(TestServeExampleMongoDB,'test_serve_mongodb_'+test['name'],exec_func)
   
#############################################################################

            
if __name__ == '__main__':

    ap = argparse.ArgumentParser(description="Optimade Example MongoDB tests")
    args, leftovers = ap.parse_known_args()
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestServeExampleMongoDB)
    unittest.TextTestRunner(verbosity=4).run(suite)        

    
