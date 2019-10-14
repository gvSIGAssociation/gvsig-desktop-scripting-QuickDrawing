# encoding: utf-8

import gvsig
from gvsig import geom
from org.gvsig.fmap.dal.feature import FeatureStore
from org.gvsig.fmap.mapcontext.layers.vectorial import VectorLayer

#from javax.print import STRING
from org.gvsig.fmap.dal import DALLocator

from org.gvsig.fmap.mapcontext import MapContextLocator

from org.gvsig.fmap.mapcontext.layers.vectorial import FLyrVect

def createMemoryStore():
  dataManager = DALLocator.getDataManager()
  store_parameters = dataManager.createStoreParameters("Memory")
  #store_parameters.setDynValue("isTemporary", True)
  store = dataManager.openStore("Memory")
  ft = store.getDefaultFeatureType()
  eft = ft.getEditable()
  eft.append("ID", 'STRING', 38)
  eft.get("ID").setIsPrimaryKey(True)
  eft.append("COUTLINE", "INTEGER", 9)
  eft.append("CFILL", "INTEGER", 9)
  eft.append("CSIZE", "INTEGER", 9)
  eft.append("CROTATION", "INTEGER", 9)
  
  eft.append("LTEXT", 'STRING', 150)
  eft.append("LCOLOR", 'INTEGER', 9)
  eft.append("LROTATION", 'INTEGER', 9)
  eft.append("LFONT", 'STRING', 150)
  eft.append("LFONTS", 'INTEGER', 9)
  eft.append("LHEIGHT", 'INTEGER', 5)
  eft.append("LUNIT", 'INTEGER', 2)
  eft.append("LREF", 'INTEGER', 2)
  
  eft.append("GEOMETRY", "GEOMETRY")
  eft.get("GEOMETRY").setGeometryType(geom.NULL, geom.UNKNOWN)
  store.edit()
  store.update(eft)
  store.finishEditing()  
  return store
    
def main(*args):
  print "Testing graphic memory store"
  #v = DrawGraphicLayer()
  store = createMemoryStore()

  store.edit(FeatureStore.MODE_APPEND)
  f = store.createNewFeature()
  line1 = geom.createGeometry(geom.LINE)
  line1.addVertex(geom.createPoint(geom.D2,0,0))
  line1.addVertex(geom.createPoint(geom.D2,10,10))
  f.set('ID', 1)
  f.set('GEOMETRY', line1)
  store.insert(f)
  store.finishEditing()

  store.edit()
  f.set('ID', 2)
  f.set('GEOMETRY', geom.createPoint(geom.D2,15,10))
  store.insert(f)
  
  f.set('ID', 2)
  f.set('GEOMETRY', geom.createPoint(geom.D2,15,10))
  store.insert(f)
  
  store.finishEditing()



  #load layer
  mapContextManager = MapContextLocator.getMapContextManager()
  layer = mapContextManager.createLayer('MyLayer',store)
  print layer,type(layer)
  gvsig.currentView().addLayer(layer)  

  features = store.getFeatures()
  selection = store.getFeatureSelection()
  for f in features:
    selection.select(f)
    
  store.edit()
  features = store.getFeatureSelection()
  values = {"GEOMLINE": 1}
  
  for f in features:
    fe = f.getEditable()
    print "F: ", f
    for key,value in values.iteritems():
      fe.set(key, value)
    store.update(fe)
  store.commit()