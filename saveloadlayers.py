# encoding: utf-8

import gvsig
from org.gvsig.fmap.dal import DALLocator
from org.json import JSONArray
from org.json import JSONObject
from gvsig.geom import createGeometryFromWKT
from qdlib.drawGraphicLayer import createMemoryStore
from org.gvsig.fmap.mapcontext import MapContextLocator
from addons.QuickDrawing import quickDrawingTool

def main(*args):
  view = gvsig.currentView()
  mapContext = view.getMapContext()
  if mapContext.getGraphicsLayer(quickDrawingTool.DEFAULT_DRAW_LAYER)==None:
    return
  layer = mapContext.getGraphicsLayer(quickDrawingTool.DEFAULT_DRAW_LAYER)
  l = saveGraphicsLayers(layer)
  #jsongraphicsstring = jsongraphics.toString()
  
  loadLayersGraphics(l)
  


def saveGraphicsLayers(layer):
    jsonlayer = layerToJSON(layer)
    return jsonlayer.toString()
        

def layerToJSON(layer):
  jsonlayer = JSONObject()
  jsonfeatures = JSONArray()
  ftype = layer.getFeatureStore().getDefaultFeatureType()
  geomAttributeName = ftype.getDefaultGeometryAttributeName()
  for f in layer.getFeatureStore().getFeatureSet():
    jsonfeature = JSONObject()
    values = f.getValues()
    for k in values.keys():
      value =  values[k]
      if k == geomAttributeName:
        wkt = value.convertToWKT()
        jsonfeature.putOnce(k, wkt)
      else:
        jsonfeature.putOnce(k, value)
    jsonfeatures.put(jsonfeature)
  jsonlayer.put("features", jsonfeatures)
  return jsonlayer
  
def loadLayersGraphics(jsongraphicsstring):
  jsongraphics = JSONObject(jsongraphicsstring)
  
  if jsongraphics==None:
    return
  mapContextManager = MapContextLocator.getMapContextManager()

  store = loadLayerFromJSON(jsongraphics)
  layer = mapContextManager.createLayer(quickDrawingTool.DEFAULT_DRAW_LAYER, store)

  return layer
   

def loadLayerFromJSON(jsonlayer):
  store = createMemoryStore()
  if not store.isEditing(): store.edit()
  f = store.createNewFeature()
  jsonfeatures = jsonlayer.getJSONArray("features")
  ftype = store.getDefaultFeatureType()
  geomAttributeName = ftype.getDefaultGeometryAttributeName()
  for jsonfeature in jsonfeatures:
    f = store.createNewFeature()
    for key in jsonfeature.keys():
      value = jsonfeature.get(key)
      if key == geomAttributeName: 
        if value!="":
          wktGeom = createGeometryFromWKT(value)
        else:
          wktGeom = None
        f.set(key, wktGeom)
      else:
        f.set(key, value)
    store.insert(f)
  return store