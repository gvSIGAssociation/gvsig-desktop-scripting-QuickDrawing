# encoding: utf-8

import gvsig
from gvsig import geom
from java.awt.geom import Point2D
from org.gvsig.fmap.mapcontrol.tools.Listeners import PointListener
#from org.gvsig.fmap.mapcontrol.tools.Behavior import MouseMovementBehavior
#from org.gvsig.fmap.mapcontrol.tools.Listeners import AbstractPointListener
from org.gvsig.fmap.mapcontext.layers.vectorial import SpatialEvaluatorsFactory
from org.gvsig.fmap import IconThemeHelper
from org.gvsig.fmap.mapcontrol.tools.Behavior import PointBehavior
from org.gvsig.tools import ToolsLocator
import random
from gvsig.utils import *
from org.gvsig.fmap.geom import Geometry
from org.gvsig.fmap.mapcontext import MapContextLocator

from qdbasic import QuickDrawingBasic
from java.lang import Object

class QuickDrawingSelect(QuickDrawingBasic):

  def __init__(self):
    pass

  def getTooltipValue(self, point, projection):
    return ""

  def setTool(self, mapControl):
    self.__behavior = PointBehavior(QuickDrawingSelectListener(mapControl, self))
    mapControl.addBehavior("quickdrawingselectpoint", self.__behavior)
    mapControl.setTool("quickdrawingselectpoint")


class QuickDrawingSelectListener(PointListener):

  def __init__(self, mapControl, quickdrawing):
    PointListener.__init__(self)
    self.mapControl = mapControl
    self.mapContext = self.mapControl.getMapContext()
    self.quickdrawing = quickdrawing
    self.projection = self.mapControl.getProjection()

  def point(self, event):
    p = event.getMapPoint()
    layer = self.quickdrawing.getLayer()
    layerTolerance = layer.getDefaultTolerance()
    tolerance = self.mapControl.getViewPort().toMapDistance(layerTolerance)
    pBufferTolerance = p.buffer(tolerance)
                  
    store = layer.getFeatureStore()
    store.getFeatureSelection().deselectAll()
    
    query = store.createFeatureQuery()
    viewProjection = self.mapControl.getProjection()
    query.setFilter(SpatialEvaluatorsFactory.getInstance().intersects(pBufferTolerance,viewProjection,store))
    query.retrievesAllAttributes()
    features = store.getFeatureSet(query) #,100)

    if features.getSize() == 0:
     pass
    else:
     for f in features:
      store.getFeatureSelection().select(f)
      values = f.getValues()
      self.quickdrawing.getUI().setUIValues(values)
      
    self.mapContext.invalidate()
    
  def pointDoubleClick(self, event):
    pass
    
  def getImageCursor(self):
    """Evento de PointListener"""
    return IconThemeHelper.getImage("cursor-select-by-point")

  def cancelDrawing(self):
    """Evento de PointListener"""
    return True

def main(*args):      
  viewDoc = gvsig.currentView()
  viewPanel = viewDoc.getWindowOfView()
  mapControl = viewPanel.getMapControl()
  
  reportbypoint = QuickDrawingSelect()
  reportbypoint.setTool(mapControl)
  
