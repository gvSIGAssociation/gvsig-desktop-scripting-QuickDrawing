# encoding: utf-8

import gvsig
from gvsig import geom
from java.awt.geom import Point2D
from org.gvsig.fmap.mapcontrol.tools.Listeners import RectangleListener
#from org.gvsig.fmap.mapcontrol.tools.Behavior import MouseMovementBehavior
#from org.gvsig.fmap.mapcontrol.tools.Listeners import AbstractPointListener
from org.gvsig.fmap.mapcontext.layers.vectorial import SpatialEvaluatorsFactory
from org.gvsig.fmap import IconThemeHelper
from org.gvsig.fmap.mapcontrol.tools.Behavior import RectangleBehavior
from org.gvsig.tools import ToolsLocator
import random
from gvsig.utils import *
from org.gvsig.fmap.geom import Geometry
from org.gvsig.fmap.mapcontext import MapContextLocator

from qdbasic import QuickDrawingBasic
from java.lang import Object

class QuickDrawingRectangleFill(QuickDrawingBasic):

  def __init__(self):
    QuickDrawingBasic.__init__(self)

  def getTooltipValue(self, point, projection):
    return ""

  def setTool(self, mapControl):
    self.__behavior = RectangleBehavior(QuickDrawingRectangleFillListener(mapControl, self))
    mapControl.addBehavior("quickdrawingrectanglefill", self.__behavior)
    mapControl.setTool("quickdrawingrectanglefill")


class QuickDrawingRectangleFillListener(RectangleListener):

  def __init__(self, mapControl, quickdrawing):
    RectangleListener.__init__(self)
    self.mapControl = mapControl
    self.mapContext = self.mapControl.getMapContext()
    self.quickdrawing = quickdrawing
    self.projection = self.mapControl.getProjection()

  def rectangle(self, event):
    p = event.getWorldCoordRect()
    try:
      pBufferTolerance = p.getGeometry().toPolygons() #.toLines() #.buffer(tolerance)
    except:
      return
    projection = self.mapControl.getProjection()
    pBufferTolerance.setProjection(projection)
    self.quickdrawing.addGraphic(pBufferTolerance)
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
  
  reportbypoint = QuickDrawingRectangleFill()
  reportbypoint.setTool(mapControl)
  
