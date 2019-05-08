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

import pymongo
import threading



class Database(object): 

    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client.optimade_test
        
    def empty_database(self):
        self.client.drop_database("optimade_test")
        self.db = self.client.optimade_test
        
    def collection_destroy_if_exists(self,coll):
        self.db[coll].remove({})
        if coll in self.db.list_collection_names():
            self.db[coll].drop()
    
    def insert(self,coll,data):
        self.db[coll].insert_one(data)

    def insert_many(self,coll,datas):
        try:
            x = self.db[coll].insert_many(datas)
        except pymongo.errors.BulkWriteError as e:
            print(e.details)
            raise
            
    def find(self,coll,query,projection=None, limit = None):
        if projection is None or projection == []:
            if limit is None:
                return self.db[coll].find(query)
            else:
                return self.db[coll].find(query).limit(limit)
        else:
            if limit is None:
                return self.db[coll].find(query,dict([(x,1) for x in projection]))
            else:
                return self.db[coll].find(query,dict([(x,1) for x in projection])).limit(limit)

    def find_one(self,coll,query):
        return self.db[coll].find_one(query)    
            
    def close(self):
        self.client.close()

