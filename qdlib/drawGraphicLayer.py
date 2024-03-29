# encoding: utf-8

import gvsig
from gvsig import geom
from org.gvsig.fmap.dal.feature import FeatureStore
from org.gvsig.fmap.mapcontext.layers.vectorial import VectorLayer

#from javax.print import STRING
from org.gvsig.fmap.dal import DALLocator

from org.gvsig.fmap.mapcontext import MapContextLocator

from org.gvsig.fmap.mapcontext.layers.vectorial import FLyrVect
from org.gvsig.fmap.geom import Geometry

def createMemoryStore():
  dataManager = DALLocator.getDataManager()
  store_parameters = dataManager.createStoreParameters("Memory")
  store_parameters.setDynValue("isTemporary", True)
  store = dataManager.openStore("Memory")
  ft = store.getDefaultFeatureType()
  eft = ft.getEditable()
  eft.append("ID", 'STRING', 38)
  eft.get("ID").setIsPrimaryKey(True)
  eft.get("ID").setDefaultFieldValue("<%=replace(UUID(),'-','')%>")
  eft.append("COUTLINE", "INTEGER", 9)
  eft.get("COUTLINE").setDefaultValue(16724787)
  
  eft.append("CFILL", "INTEGER", 9)
  eft.get("CFILL").setDefaultValue(-65536)
  
  eft.append("CSIZE", "INTEGER", 9)
  eft.get("CSIZE").setDefaultValue(2)
  
  eft.append("CROTATION", "INTEGER", 9)
  eft.get("CROTATION").setDefaultValue(0)
  
  eft.append("LTEXT", 'STRING', 150)
  eft.get("LTEXT").setDefaultValue("")
  eft.append("LCOLOR", 'INTEGER', 9)
  eft.get("LCOLOR").setDefaultValue(1258291200)
  eft.append("LROTATION", 'INTEGER', 9)
  eft.get("LROTATION").setDefaultValue(0)
  eft.append("LFONT", 'STRING', 150)
  eft.get("LFONT").setDefaultValue("Serif")
  eft.append("LFONTS", 'INTEGER', 9)
  eft.get("LFONTS").setDefaultValue(0)
  eft.append("LHEIGHT", 'INTEGER', 5)
  eft.get("LHEIGHT").setDefaultValue(10)
  eft.append("LUNIT", 'INTEGER', 2)
  eft.get("LUNIT").setDefaultValue(1)
  eft.append("LREF", 'INTEGER', 2)
  eft.get("LREF").setDefaultValue(0)
  
  eft.append("GEOMETRY", "GEOMETRY")
  eft.get("GEOMETRY").setGeometryType(Geometry.TYPES.GEOMETRY, Geometry.SUBTYPES.GEOM2D)
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