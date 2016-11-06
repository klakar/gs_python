# -*- coding: utf-8 -*-
"""
This module has three functions:
- newDataset(EPSG[int], filename[string], filetype[string], attributename[lista-string], attributetype[list-ogr.OFTxxx])
- addPoint(datalayer[ogr layer], X[number], Y[number], attributename[list-string], attributevalue[list])
- closeDataset(dataset)

The Function "newDataset()" returns two objects.
- One dataset and
- One layer
Example:
my_dataset, my_layer = newDataset(.....)
"""

# Import GDAL/OGR to be able to create datasets and layers
from osgeo import ogr, osr

# Help function
def help():
   print("Syntax:")
   print("newDataset(filename, filetype, EPSG, attribute_name_list, attribute_type_list)")
   print("Attribute type is ogr.OFTString, ogr.OFTInteger, etc")
   print("Function returns tuple with dataset-object and layer-object")
   print("\naddPoint(layer-object, x-coordinate, y-coordinate, attribute_name_list, attribute_value_list)")
   print("Function doesn't return anything.\n")
   print("closeDataset(dataset-object)")
   print("Function close a created dataset")

# The function creates a dataset, and a layer with a set of attributes
# filename is a path to the dataset to create (relative paths ok)
# filetype is the ogr Driver name i.e. "GPKG", "ESRI Shapefile", etc
# EPSG is an integer (ex 4326)
# attrName is a list with strings representing the attribute names
# attrType is a list with ogr.OFTString, ogr.OFTReal, ogr.OFTInteger, or equivalent.
# The important thing is that attrName and attrType is of equal length.
# The function returns a "tuple" with a dataset and a layer object (ds, lr = newDataset(...))
def newDataset(filename, filetype, EPSG, attrName, attrType):
   gpkgDrv = ogr.GetDriverByName(filetype)
   dS = gpkgDrv.CreateDataSource(filename)
   srs = osr.SpatialReference()
   srs.ImportFromEPSG(EPSG)
   lr = dS.CreateLayer(filename, srs, ogr.wkbPoint)
   for a_name, a_type in zip(attrName, attrType):
     fD = ogr.FieldDefn(a_name, a_type)
     lr.CreateField(fD)
   return(dS, lr)

# The function adds a point with position and attribute to layer "lr".
# The function can be repeated as many times as necessary, once for every point.
# The important thing is that the lists for name and value is of equal lentgh.
def addPoint(lr, lon, lat, attrName, attrValue):
   lD = lr.GetLayerDefn()
   ft = ogr.Feature(lD)
   p = ogr.Geometry(ogr.wkbPoint)
   p.AddPoint(lon, lat)
   ft.SetGeometry(p)
   for a_name, a_value in zip(attrName, attrValue):
     ft.SetField(a_name, a_value)
   lr.CreateFeature(ft)

# The function close the dataset "dS"
def closeDataset(dS):
   dS.Destroy()
