# encoding: utf-8

import gvsig
from gvsig import geom
from java.awt.geom import Point2D
from org.gvsig.fmap.mapcontrol.tools.Listeners import AbstractCircleListener
from org.gvsig.fmap.mapcontext.layers.vectorial import SpatialEvaluatorsFactory
from org.gvsig.fmap import IconThemeHelper
from org.gvsig.fmap.mapcontrol.tools.Behavior import CircleBehavior
from org.gvsig.tools import ToolsLocator
import random
from gvsig.utils import *
from org.gvsig.fmap.geom import Geometry
from org.gvsig.fmap.mapcontext import MapContextLocator
import random
from org.gvsig.fmap.dal.feature import FeatureStore

from qdbasic import QuickDrawingBasic

class QuickDrawingCircumference(QuickDrawingBasic):

  def __init__(self):
    QuickDrawingBasic.__init__(self)
    
  def getTooltipValue(self, point, projection):
    return ""

  def setTool(self, mapControl):
    self.behavior = CircleBehavior(QuickDrawingCircumferenceListener(mapControl, self))
    mapControl.addBehavior("quickdrawingpolyline", self.behavior)
    mapControl.setTool("quickdrawingpolyline")


class QuickDrawingCircumferenceListener(AbstractCircleListener):

  def __init__(self, mapControl, quickdrawing):
    AbstractCircleListener.__init__(self)
    self.mapControl = mapControl
    self.mapContext = self.mapControl.getMapContext()
    self.quickdrawing = quickdrawing
    self.projection = self.mapControl.getProjection()
    
  def getImageCursor(self):
    """Evento de PointListener"""
    
    return IconThemeHelper.getImage("cursor-select-by-point")

  def cancelDrawing(self):
    """Evento de PointListener"""
    return False
  def circleFinished(self, event):
    circle = event.getCircumference()
    if circle!=None:
      projection = self.mapControl.getProjection()
      circle.setProjection(projection)
      self.quickdrawing.addGraphic(circle)
      self.mapContext.invalidate()
      
  def circle(self, event):
    pass

def main(*args):      
  viewDoc = gvsig.currentView()
  viewPanel = viewDoc.getWindowOfView()
  mapControl = viewPanel.getMapControl()
  
  reportbypoint = QuickDrawingCircumference()
  reportbypoint.setTool(mapControl)
  
