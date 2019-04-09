# encoding: utf-8

import gvsig
from gvsig import geom
from java.awt.geom import Point2D
from org.gvsig.fmap.mapcontrol.tools.Listeners import PolylineListener
from org.gvsig.fmap.mapcontext.layers.vectorial import SpatialEvaluatorsFactory
from org.gvsig.fmap import IconThemeHelper
from org.gvsig.fmap.mapcontrol.tools.Behavior import PolylineBehavior
from org.gvsig.tools import ToolsLocator
import random
from gvsig.utils import *
from org.gvsig.fmap.geom import Geometry
from org.gvsig.fmap.mapcontext import MapContextLocator
import random
from org.gvsig.fmap.dal.feature import FeatureStore

class QuickDrawingPolyline(object):

  def __init__(self):
    self.behavior = None
    self.store = None
    
  def setStore(self, store):
    self.store = store
    
  def getStore(self):
    return self.store
    
  def getTooltipValue(self, point, projection):
    return ""

  def setTool(self, mapControl):
    self.behavior = PolylineBehavior(QuickDrawingPolylineListener(mapControl, self))
    mapControl.addBehavior("quickdrawingpolyline", self.behavior)
    mapControl.setTool("quickdrawingpolyline")

  def addGraphic(self, geometry):
    self.store.edit() #FeatureStore.MODE_APPEND)
    f = self.store.createNewFeature()
    f.set('ID', random.randint(0,200000))
    f.set('GEOMETRY', geometry)
    self.store.insert(f)
    self.store.finishEditing()

class QuickDrawingPolylineListener(PolylineListener):

  def __init__(self, mapControl, quickdrawing):
    PolylineListener.__init__(self)
    self.mapControl = mapControl
    self.mapContext = self.mapControl.getMapContext()
    self.graphicsLayer = self.mapContext.getGraphicsLayer() #"quickdrawing")
    self.quickdrawing = quickdrawing
    self.projection = self.mapControl.getProjection()

  def points(self, event):
    #self.mapContext.invalidate()
    pass
    
  def pointDoubleClick(self, event):
    pass
    
  def getImageCursor(self):
    """Evento de PointListener"""
    return IconThemeHelper.getImage("layout-graphic-edit-vertex")
    #return IconThemeHelper.getImage("cursor-select-by-point")

  def cancelDrawing(self):
    """Evento de PointListener"""
    return True
    
  def polylineFinished(self, event):
    print "finished"
    x = event.getXs()
    y = event.getYs()
    line = geom.createGeometry(geom.LINE, geom.D2)
    for coord in zip(x, y):
      point = geom.createPoint(geom.D2, coord[0], coord[1])
      line.addVertex(point)
    print "Final line: ", line
    self.quickdrawing.addGraphic(line)
    
    
  def pointFixed(self, event):
    print "fixed"


def main(*args):      
  viewDoc = gvsig.currentView()
  viewPanel = viewDoc.getWindowOfView()
  mapControl = viewPanel.getMapControl()
  
  reportbypoint = QuickDrawingPolyline()
  reportbypoint.setTool(mapControl)
  
