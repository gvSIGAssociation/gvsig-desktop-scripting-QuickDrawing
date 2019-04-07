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

class QuickDrawingPoint(object):

  def __init__(self):
    self.__behavior = None
    self.__layer = None

  def getTooltipValue(self, point, projection):
    return ""

  def setTool(self, mapControl):

    #if len(actives)!=1:
    #  # Solo activamos la herramienta si hay una sola capa activa
    #  #print "### reportbypoint.setTool: active layers != 1 (%s)" % len(actives)
    #  return
    #mode = actives[0].getProperty("reportbypoint.mode")
    #if mode in ("", None):
    #  # Si la capa activa no tiene configurado el campo a mostrar
    #  # tampoco activamos la herramienta
    #  #print '### reportbypoint.setTool: active layer %s not has property "reportbypoint.fieldname"' % actives[0].getName()
    #  return 

    #if it has the tool
    #if not mapControl.hasTool("quickdrawingpoint"):
      #print '### QuickInfo.setTool: Add to MapControl 0x%x the "quickinfo" tool' % mapControl.hashCode()
      #
      # Creamos nuestro "tool" asociando el MouseMovementBehavior con nuestro
      # QuickInfoListener.
      #self.__behavior = MouseMovementBehavior(ReportByPointListener(mapControl, self))
    self.__behavior = PointBehavior(QuickDrawingPointListener(mapControl, self))
    #self.__behavior.setMapControl(mapControl)    
    #
    # Le añadimos al MapControl la nueva "tool".
    mapControl.addBehavior("quickdrawingpoint", self.__behavior)
    #print '### QuickInfo.setTool: setTool("quickinfo") to MapControl 0x%x' % mapControl.hashCode()
    #
    # Activamos la tool.
    
    mapControl.setTool("quickdrawingpoint")


class QuickDrawingPointListener(PointListener):

  def __init__(self, mapControl, quickdrawingpoint):
    PointListener.__init__(self)
    self.mapControl = mapControl
    self.mapContext = self.mapControl.getMapContext()
    self.graphicsLayer = self.mapContext.getGraphicsLayer() #"quickdrawing")
    #if self.graphicsLayer==None:
    #  tracLayer = MapContextLocator.getMapContextManager().createGraphicsLayer(None)
    #  self.mapContext.setGraphicsLayer("quickdrawing", tracLayer)
    self.quickdrawingpoint = quickdrawingpoint
    self.projection = self.mapControl.getProjection()

  def point(self, event):
    p = event.getMapPoint()
    print "drawing point:", p, type(p)
    if self.graphicsLayer==None:
      print "null graphics"
      return
    print "continue"
    self.graphicsLayer.removeGraphics("ejemplo")
    print "removed"
    r = lambda: random.randint(0, 255)
    color = getColorFromRGB(r(), r(), r() ,r())
    point = MapContextLocator.getSymbolManager().createSymbol(Geometry.TYPES.POINT, color)
    idPolSymbol = self.graphicsLayer.addSymbol(point)
    self.graphicsLayer.addGraphic("ejemplo", p,  idPolSymbol, "Label")
    self.mapContext.invalidate()
    
  def pointDoubleClick(self, event):
    pass
    
  def getImageCursor(self):
    """Evento de PointListener"""
    return IconThemeHelper.getImage("cursor-select-by-point")

  def cancelDrawing(self):
    """Evento de PointListener"""
    print "cancel"
    return False

def main(*args):      
  viewDoc = gvsig.currentView()
  viewPanel = viewDoc.getWindowOfView()
  mapControl = viewPanel.getMapControl()
  
  reportbypoint = QuickDrawingPoint()
  reportbypoint.setTool(mapControl)
  
