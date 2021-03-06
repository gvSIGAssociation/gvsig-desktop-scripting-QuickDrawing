# encoding: utf-8

import gvsig
from gvsig import geom
from java.awt.geom import Point2D
from org.gvsig.fmap.mapcontrol.tools.Listeners import PolylineListener
from org.gvsig.fmap.mapcontext.layers.vectorial import SpatialEvaluatorsFactory
from org.gvsig.fmap import IconThemeHelper
from org.gvsig.fmap.mapcontrol.tools.Behavior import PolygonBehavior
from org.gvsig.tools import ToolsLocator
import random
from gvsig.utils import *
from org.gvsig.fmap.geom import Geometry
from org.gvsig.fmap.mapcontext import MapContextLocator
import random
from org.gvsig.fmap.dal.feature import FeatureStore

from qdbasic import QuickDrawingBasic

class QuickDrawingPolylineClosed(QuickDrawingBasic):

  def __init__(self):
    QuickDrawingBasic.__init__(self)
    
  def getTooltipValue(self, point, projection):
    return ""

  def setTool(self, mapControl):
    self.behavior = PolygonBehavior(QuickDrawingPolylineClosedListener(mapControl, self))
    mapControl.addBehavior("quickdrawingpolylineclosed", self.behavior)
    mapControl.setTool("quickdrawingpolylineclosed")


class QuickDrawingPolylineClosedListener(PolylineListener):

  def __init__(self, mapControl, quickdrawing):
    PolylineListener.__init__(self)
    self.mapControl = mapControl
    self.mapContext = self.mapControl.getMapContext()
    self.quickdrawing = quickdrawing
    self.projection = self.mapControl.getProjection()
  
  def points(self, event):
    pass
    
  def pointDoubleClick(self, event):
    pass
    
  def getImageCursor(self):
    """Evento de PointListener"""
    
    return IconThemeHelper.getImage("cursor-select-by-point")

  def cancelDrawing(self):
    """Evento de PointListener"""
    return True
    
  def polylineFinished(self, event):
    x = event.getXs()
    y = event.getYs()
    if len(x)<2:
      return
    line = geom.createGeometry(geom.LINE, geom.D2)
    for coord in zip(x, y):
      point = geom.createPoint(geom.D2, coord[0], coord[1])
      line.addVertex(point)
    line.addVertex(x[0], y[0])
    projection = self.mapControl.getProjection()
    line.setProjection(projection)
    self.quickdrawing.addGraphic(line)
    self.mapContext.invalidate()
    
    
  def pointFixed(self, event):
    pass


def main(*args):      
  viewDoc = gvsig.currentView()
  viewPanel = viewDoc.getWindowOfView()
  mapControl = viewPanel.getMapControl()
  
  reportbypoint = QuickDrawingPolylineClosed()
  reportbypoint.setTool(mapControl)
  
