# encoding: utf-8

import gvsig
from gvsig import geom
from java.awt.geom import Point2D
from org.gvsig.fmap.mapcontrol.tools.Listeners import EllipseListener
from org.gvsig.fmap.mapcontext.layers.vectorial import SpatialEvaluatorsFactory
from org.gvsig.fmap import IconThemeHelper
from org.gvsig.fmap.mapcontrol.tools.Behavior import EllipseBehavior
from org.gvsig.tools import ToolsLocator
import random
from gvsig.utils import *
from org.gvsig.fmap.geom import Geometry
from org.gvsig.fmap.mapcontext import MapContextLocator
import random
from org.gvsig.fmap.dal.feature import FeatureStore

from qdbasic import QuickDrawingBasic

class QuickDrawingEllipseFill(QuickDrawingBasic):

  def __init__(self):
    QuickDrawingBasic.__init__(self)
    
  def getTooltipValue(self, point, projection):
    return ""

  def setTool(self, mapControl):
    self.behavior = EllipseBehavior(QuickDrawingEllipseFillListener(mapControl, self))
    mapControl.addBehavior("quickdrawingellipsefill", self.behavior)
    mapControl.setTool("quickdrawingellipsefill")


class QuickDrawingEllipseFillListener(EllipseListener):

  def __init__(self, mapControl, quickdrawing):
    EllipseListener.__init__(self)
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
    
  def ellipseFinished(self, event):
    circle = event.getEllipse()
    if circle!=None:
      projection = self.mapControl.getProjection()
      circle.setProjection(projection)
      self.quickdrawing.addGraphic(circle)
      self.mapContext.invalidate()
      
  def circle(self, event):
    pass
  def ellipse(self, event):
    pass

def main(*args):      
  viewDoc = gvsig.currentView()
  viewPanel = viewDoc.getWindowOfView()
  mapControl = viewPanel.getMapControl()
  
  reportbypoint = QuickDrawingEllipseFill()
  reportbypoint.setTool(mapControl)
  
