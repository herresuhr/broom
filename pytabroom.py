from tables import *
import numpy as np


def pytasave(fn, sw):
 """
 Saves the default parameters, the looped parameters and the results in fn.h5
 """

 # Open hdf5 file and initialize data structure
 tabl = pytastruct(sw)
 
 h5fn = openFile(fn + ".h5", mode = "w", title = "Sweeped data")
 root = h5fn.root
 tab1 = h5fn.createTable(root, 'tab1', tabl, 'Data')

 # Fill in meta data
 parkeys = sw.default_params[0].keys()
 for key in parkeys:
  tab1.attrs.tmp = sw.default_params[0][key]
  tab1.attrs._f_rename("tmp", key)
 
 tab1.flush() 

 # Fill in data
 parkeys = sw.sweep_dict.keys()
 res     = sw.results
 reskeys = res.keys()
 for key in reskeys:
  res[key].shape = -1
 
 dset = tab1.row
 for n in range(len(sw.params)):
  for m, key in enumerate(parkeys):
   dset[key] = sw.params[n][m]
  
  for key in reskeys:
   dset[key] = res[key][n]
 
  dset.append()

 tab1.flush()

 # Save and close
 h5fn.close()
 return

def pytastruct(sw):
 """
 Define data structure based on input
 """
 
 parkeys = sw.sweep_dict.keys()
 reskeys = sw.results.keys()
 
 # Set up string containing definitions of names and data types
 pytatype = {"<type 'float'>":"Float64Col", "<type 'int'>":"Int32Col", "<type 'long'>":"Int64Col"}
 
 tabdef = "class tabl(IsDescription):"
 for n, key in enumerate(parkeys):
  vals   = sw.sweep_dict[key]
  tabdef = tabdef + "\n " + key + " = " + pytatype[repr(type(vals[0]))] + "()"
				  
 for n, key in enumerate(reskeys):
  vals   = sw.results[key][0]
  tabdef = tabdef + "\n " + key + " = " + pytatype[repr(type(vals[0]))] + "()"

 # Execute and return data structure definition
 exec tabdef 
 return tabl