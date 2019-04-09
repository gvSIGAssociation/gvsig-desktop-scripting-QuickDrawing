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
  store = dataManager.openStore("Memory")
  ft = store.getDefaultFeatureType()
  eft = ft.getEditable()
  eft.append("ID", 'INTEGER', 9)
  eft.get("ID").setIsPrimaryKey(True)
  
  eft.append("CLRLINE", "STRING", 30)
  eft.append("CLRFILL", "STRING", 30)
  eft.append("LBLTXT", 'STRING', 150)
  eft.append("LBLCOLOR", 'STRING', 30)
  eft.append("LBLFONT", 'STRING', 150)
  eft.append("LBLSIZE", 'INTEGER', 5)
  eft.append("GEOMETRY", "GEOMETRY")
  eft.get("GEOMETRY").setGeometryType(geom.NULL, geom.UNKNOWN)
  store.edit()
  store.update(eft)
  store.finishEditing()  
  return store
  
class DrawGraphicLayer(FLyrVect): #VectorLayer):
  def __init__(self):
    self.store = None
   
    
  def setBaseQuery(self, baseQuery):
    pass
    
  def getBaseQuery(self): # FeatureQuery
    return 
    
  def addBaseFilter(self, filter): # params: Evaluator or String
    pass
    
  def createFeatureQuery(self): # FeatureQuery
    pass
    
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
