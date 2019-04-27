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
    def __init__(self, id, lattice_vectors, cartesian_site_positions, species_at_sites, species, assemblies = None,  chemical_formula = None, cifdata = None, local_id = None, modification_date = None):

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

        formula_components = {}
        for entry in species_at_sites:
            for element, occupancy in zip(species[entry]['chemical_symbols'],species[entry]['concentration']):
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

        prototype_formula_components = re.findall('([A-Z][a-z]?)([0-9.]*)',self.chemical_formula)
        prototype_formula_components = sorted([(float(occ),occ) if occ != '' else (1.0,'') for el,occ in prototype_formula_components])
        prototype_formula_components = [int_to_anonymous_symbol(i)+prototype_formula_components[i][1] for i in range(len(prototype_formula_components))]
        self.formula_prototype = "".join(prototype_formula_components)

        if modification_date is not None:
            self.modification_date = modification_date
        else:
            self.modification_date = datetime.datetime.now().isoformat()

    def __str__(self):
        return "<OptimadeStructure:"+self.chemical_formula+">"

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

            
json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'json')

def str_to_float(x):
    return float(x.replace('(','').replace(')',''))

def cif_to_structs(cif):
    #pprint.pprint(cif)
    header = cif[1]
    structs = []

    for c in cif[0]:
        id = c[0]
        data = c[1]

        # Lattice vectors (We don't do the conventional cell right now)
        alpha = str_to_float(data['cell_angle_alpha'])
        beta = str_to_float(data['cell_angle_beta'])
        gamma = str_to_float(data['cell_angle_gamma'])
        a = str_to_float(data['cell_length_a'])
        b = str_to_float(data['cell_length_b'])
        c = str_to_float(data['cell_length_c'])

        cosalpha = math.cos(math.radians(alpha))
        cosbeta = math.cos(math.radians(beta))
        cosgamma = math.cos(math.radians(gamma))
        singamma = math.sqrt(1.0-cosgamma**2)
        angfac1 = (cosalpha - cosbeta*cosgamma)/singamma
        angfac2 = math.sqrt(singamma**2 - cosbeta**2 - cosalpha**2 + 2.0*cosalpha*cosbeta*cosgamma)/singamma
        lattice_vectors = [[a, 0, 0], [b*cosgamma, b*singamma, 0], [c*cosbeta, c*angfac1, c*angfac2]]
        
        # Coords
        all_coords = list(zip(data['atom_site_fract_x'], data['atom_site_fract_y'], data['atom_site_fract_z']))
        all_uniq_coords = []
        mapper = [None]*len(all_coords)
        j = 0
        for i in range(len(all_coords)):
            coord = all_coords[i]
            try:
                j = all_uniq_coords.index(coord)
                mapper[i] = j            
            except ValueError:
                all_uniq_coords += [[str_to_float(x) for x in coord]]
                mapper[i] = j
                j += 1
        ncoords = len(all_uniq_coords)
            
        l = lattice_vectors
        cartesian_site_positions = [(ra*l[0][0]+rb*l[0][1]+rc*l[0][2],ra*l[1][0]+rb*l[1][1]+rc*l[1][2],ra*l[2][0]+rb*l[2][1]+rc*l[2][2]) for ra,rb,rc in all_uniq_coords]

        # Sites and occupencies, this is a bit tricky to assemble due to cifs using repeat coordinates for sites with disordered occupancy
        species_at_sites_list = [ [] for i in range(ncoords)]             
        for i in range(len(data['atom_site_label'])):
            species_at_sites_list[mapper[i]] += [str(re.match('[A-Z][a-z]?',data['atom_site_label'][i]).group(0))]

        if 'atom_site_occupancy' in data:
            occupancies_at_sites_list = [ [] for i in range(ncoords)]
            for i in range(len(data['atom_site_occupancy'])):
                occupancies_at_sites_list[mapper[i]] += [data['atom_site_occupancy'][i]]
        else:
             occupancies_at_sites_list = ["1"]*ncoords

        species = {}
        species_at_sites = []
        for elems, occups in zip(species_at_sites_list, occupancies_at_sites_list):
            #if len(occups) == 1 and abs(float(occups[0])-1.0)<1e-6:
            #    name = elems[0]
            #else:
            name = "__".join([el+"_"+occ for el,occ in zip(elems, occups)])
            species_at_sites += [name]
            if name not in species:
                species[name] = {'chemical_symbols':elems, 'concentration':[float(x) for x in occups]}                

        # Assemblies
        if ('atom_site_disorder_group' in data and data['atom_site_disorder_group'] != [data['atom_site_disorder_group'][0]]*len(data['atom_site_disorder_group'])) or ('atom_site_disorder_assembly' in data and data['atom_site_disorder_assembly'] != [data['atom_site_disorder_assembly'][0]]*len(data['atom_site_disorder_assembly'])):
            raise Exception("Assemblies are not yet supported.")
        else:
            assemblies = None
        
        #print("ID",id)
        #print("species at sites:",species_at_sites)
        #print("speices_types",species)
        #print("lattice_vetors",lattice_vectors)
        #print("cartesian_site_positions",cartesian_site_positions)

        #print("-------------")
        #print("COD:"+str(id))
        #print("1")
        #print(lattice_vectors[0][0],lattice_vectors[0][1],lattice_vectors[0][2])
        #print(lattice_vectors[1][0],lattice_vectors[1][1],lattice_vectors[1][2])
        #print(lattice_vectors[2][0],lattice_vectors[2][1],lattice_vectors[2][2])        
        #print(" ".join(species_at_sites))
        #print(" ".join(["1"]*len(species_at_sites)))
        #print("C")
        #print("\n".join([str(x)+" "+str(y)+" "+str(z) for x,y,z in cartesian_site_positions]))
        #print("-------------")

        structs += [OptimadeStructure("testdata_cod:"+id,lattice_vectors, cartesian_site_positions, species_at_sites, species, assemblies, cifdata=data)]
        
    return structs
    
def get_test_structures():
    structs = []
    for f in os.listdir(json_path):
        if f.endswith(".json"):
            with open(os.path.join(json_path,f),'r') as inf:
                cif = json.load(inf)
                structs += cif_to_structs(cif)
    return structs

if __name__ == "__main__":
    structs = get_test_structures()
    print("\n".join([str(x) for x in structs]))
