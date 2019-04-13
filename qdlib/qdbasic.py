# encoding: utf-8

import gvsig
from java.util import UUID

class QuickDrawingBasic(object):

  def __init__(self):
    self.behavior = None
    self.store = None
    self.ui = None
    self.layer = None
    
  def setStore(self, store):
    self.store = store
    
  def getStore(self):
    return self.store
    
  def getLayer(self):
    return self.layer
    
  def setLayer(self, layer):
    self.layer = layer
    self.setStore(self.layer.getFeatureStore())
    
  def getTooltipValue(self, point, projection):
    return ""

  def setTool(self, mapControl):
    pass
    
  def getUIValues(self):
    return self.ui.graphicValues()
    
  def getUI(self):
    return self.ui
    
  def setUI(self, ui):
    self.ui=ui
    
  def addGraphic(self, geometry):
    print "addGraphic:", geometry
    print " to: ", self.store
    values = self.getUIValues()
    if self.store==None:
      return
    if not self.store.isEditing(): self.store.edit()
    f = self.store.createNewFeature()
    for key,value in values.iteritems():
      f.set(key, value)
    f.set('ID', UUID.randomUUID().toString())
    f.set('GEOMETRY', geometry)
    self.store.insert(f)
    #self.store.finishEditing()

    
def main(*args):

    #Remove this lines and add here your code

    print "hola mundo"
    pass
