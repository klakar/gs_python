# -*- coding: utf-8 -*-
"""
This module has three functions:
  newDataset(filename[string], filetype[string], EPSG[int],
             attributename[lista-string], attributetype[list-ogr.OFTxxx])

  addPoint(datalayer[ogr layer], X[number], Y[number],
             attributename[list-string], attributevalue[list])

  closeDataset(dataset)

The Function "newDataset()" returns two objects.
- One dataset and
- One layer

Example:

my_dataset, my_layer = newDataset(.....)

"""

# Import GDAL/OGR to be able to create datasets and layers
from osgeo import ogr, osr


def newDataset(filename, filetype, EPSG, attrName, attrType):
   """
   Description:
      Returns a tuple with dataset and layer created from
      a set of arguments.
   Args:
      filename: absolute or relative path to file to create.
      filetype: ogr driver like "GPKG" or "ESRI Shapefile"
      EPSG: number like 4326
      attrName: list with attribute names for the dataset.
      attrType: list with ogr.OFT-types (ogr.OFTString, etc)
   Returns:
      dataset: dataset-object
      layer: layer-object
   Usage:
      ds, lr = newDataset(fn, ft, EPSG, attrName, attrType)
   """
   gpkgDrv = ogr.GetDriverByName(filetype)
   dS = gpkgDrv.CreateDataSource(filename)
   srs = osr.SpatialReference()
   srs.ImportFromEPSG(EPSG)
   lr = dS.CreateLayer(filename, srs, ogr.wkbPoint)
   for a_name, a_type in zip(attrName, attrType):
     fD = ogr.FieldDefn(a_name, a_type)
     lr.CreateField(fD)
   return(dS, lr)

def addPoint(lr, lon, lat, attrName, attrValue):
   """
   Description:
      Add a point with attributes to a layer
   Args:
      lr: layer-object
      lon: X coordinate
      lat: Y coordinate
      attrName: list with attribute names for the dataset.
      attrValue: list with attribute values for the point.
   Returns:
      Nothing!
   Usage:
      addPoint(lr, X, Y, attrName, attrValue)
   """
   lD = lr.GetLayerDefn()
   ft = ogr.Feature(lD)
   p = ogr.Geometry(ogr.wkbPoint)
   p.AddPoint(lon, lat)
   ft.SetGeometry(p)
   for a_name, a_value in zip(attrName, attrValue):
     ft.SetField(a_name, a_value)
   lr.CreateFeature(ft)

def closeDataset(dS):
   """
   Description:
      The function close the dataset
   Args:
      dS: dataset-object
   Returns:
      Nothing!
   Usage:
      closeDataset(dS)
   """
   dS.Destroy()
