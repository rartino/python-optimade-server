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

import os, json, pprint, re, math, datetime


def int_to_anonymous_symbol(i):
    bigletters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    smalletters = "abcdefghijklmnopqrstuvwxyz"
    if i <= 25:
        return bigletters[i]
    high = int(i/26)-1
    low = i % 26
    return bigletters[high]+smalletters[low]


class OptimadeStructure(object):
    def __init__(self, id, lattice_vectors, cartesian_site_positions, species_at_sites, species, assemblies=None, chemical_formula=None, cifdata=None, cifheader=None, local_id=None, modification_date=None):

        self.id = id
        if local_id is not None:
            self.local_id = local_id
        else:
            self.local_id = id            

        self.lattice_vectors = lattice_vectors
        self.cartesian_site_positions = cartesian_site_positions
        self.species_at_sites = species_at_sites
        self.species = species
        self.assemblies = assemblies
        self.cifdata = cifdata
        self.cifheader = cifheader

        formula_components = {}
        for entry in species_at_sites:
            for element, occupancy in zip(species[entry]['chemical_symbols'], species[entry]['concentration']):
                if element in formula_components:
                    formula_components[element] += occupancy
                else:
                    formula_components[element] = occupancy
        self.nelements = len(formula_components)
        self.elements = ",".join(formula_components.keys())

        if chemical_formula is not None:
            self.chemical_formula = chemical_formula
        else:
            formula_components_order = sorted(formula_components, key=formula_components.get)
            self.chemical_formula = "".join([x + "%g" % formula_components[x] for x in formula_components_order])

        prototype_formula_components = re.findall('([A-Z][a-z]?)([0-9.]*)', self.chemical_formula)
        prototype_formula_components = sorted([(float(occ), occ) if occ != '' else (1.0, '') for el, occ in prototype_formula_components])
        prototype_formula_components = [int_to_anonymous_symbol(i)+prototype_formula_components[i][1] for i in range(len(prototype_formula_components))]
        self.formula_prototype = "".join(prototype_formula_components)

        if modification_date is not None:
            self.modification_date = modification_date
        else:
            self.modification_date = datetime.datetime.now().isoformat()

    def __str__(self):
        return "<OptimadeStructure:"+self.id+" ("+self.chemical_formula+") >"

    def __repr__(self):
        return "OptimadeStructure("+",".join([
            "id="+repr(self.id),
            "lattice_vectors="+repr(self.lattice_vectors),
            "cartesian_site_positions="+repr(self.cartesian_site_positions),
            "species_at_sites="+repr(self.species_at_sites),
            "species="+repr(self.species),
            "assemblies="+repr(self.assemblies),
            "chemical_formula="+repr(self.chemical_formula),
            "cifdata="+repr(self.cifdata),
            "local_id="+repr(self.local_id),
            "modification_date="+repr(self.modification_date)])+")"


json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'json')


def str_to_float(x):
    return float(x.replace('(', '').replace(')', ''))


def json_to_struct(data):

    return OptimadeStructure("testdata:"+data['id'], data['lattice_vectors'], data['cartesian_site_positions'], data['species_at_sites'], data['species'], data['assemblies'], cifdata=data['cif'], cifheader=data['cif_header'])


def get_test_structures():
    structs = []
    for f in os.listdir(json_path):
        if f.endswith(".json"):
            with open(os.path.join(json_path, f), 'r') as inf:
                data = json.load(inf)
                structs += [json_to_struct(data)]
    return structs


if __name__ == "__main__":
    structs = get_test_structures()
    print("\n".join([str(x) for x in structs]))
