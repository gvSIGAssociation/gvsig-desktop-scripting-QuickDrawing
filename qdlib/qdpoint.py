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

class QuickDrawingPoint(QuickDrawingBasic):

  def __init__(self):
    QuickDrawingBasic.__init__(self)

  def getTooltipValue(self, point, projection):
    return ""

  def setTool(self, mapControl):
    self.__behavior = PointBehavior(QuickDrawingPointListener(mapControl, self))
    mapControl.addBehavior("quickdrawingpoint", self.__behavior)
    mapControl.setTool("quickdrawingpoint")


class QuickDrawingPointListener(PointListener):

  def __init__(self, mapControl, quickdrawing):
    PointListener.__init__(self)
    self.mapControl = mapControl
    self.mapContext = self.mapControl.getMapContext()
    self.quickdrawing = quickdrawing
    self.projection = self.mapControl.getProjection()

  def point(self, event):
    p = event.getMapPoint()
    #r = lambda: random.randint(0, 255)
    #color = getColorFromRGB(r(), r(), r() ,r())
    #point = MapContextLocator.getSymbolManager().createSymbol(Geometry.TYPES.POINT, color)
    #idPolSymbol = self.graphicsLayer.addSymbol(point)
    #self.graphicsLayer.addGraphic("ejemplo", p,  idPolSymbol, "Label")
    self.quickdrawing.addGraphic(p)
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
  
  reportbypoint = QuickDrawingPoint()
  reportbypoint.setTool(mapControl)
  
