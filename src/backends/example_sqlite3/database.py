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

import sqlite3
import threading

class Database(object): 

    def __init__(self):
        self.threadlocal = threading.local()
        self.threadlocal.con = sqlite3.connect(":memory:")    
        self.threadlocal.cur = self.threadlocal.con.cursor()

    def execute(self,sql, parameters={}):
        if hasattr(self.threadlocal,'cur'):
            results = self.threadlocal.cur.execute(sql, parameters) 
            data = [dict([(name[0],d) for name,d in zip(results.description, row)]) for row in results]
            return data
        else:
            raise Exception("Trying to access in-memory database across threads.")

    def commit(self):
        if hasattr(self.threadlocal,'con'):
            return self.threadlocal.con.commit()
        else:
            raise Exception("Trying to access in-memory database across threads.")
            
    def close(self):
        if hasattr(self.threadlocal,'cur'):        
            self.threadlocal.cur.close()
            self.threadlocal.con.close()
        else:
            raise Exception("Trying to access in-memory database across threads.")        

