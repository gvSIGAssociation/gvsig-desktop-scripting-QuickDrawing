# encoding: utf-8

import gvsig

from gvsig import getResource
from gvsig.libs.formpanel import FormPanel
from addons.QuickDrawing.qdlib.qdpoint import QuickDrawingPoint
from org.gvsig.tools.swing.api import ToolsSwingLocator


from qdlib.qdpolyline import QuickDrawingPolyline
from qdlib.drawGraphicLayer import createMemoryStore

from org.gvsig.fmap.mapcontext import MapContextLocator

from qdlib.drawGraphicLayer import DrawGraphicLayer

class QuickDrawingTool(FormPanel):
  DEFAULT_DRAW_LAYER = 'DEFAULT_DRAW_LAYER'
  def __init__(self):
    FormPanel.__init__(self,getResource(__file__,"quickDrawingTool.xml"))
    self.initUI()
    self.mapContext = gvsig.currentView().getMapContext()
    self.mapControl = gvsig.currentView().getWindowOfView().getMapControl()
    print "working.."
    #if self.mapContext.getGraphicsLayer(self.DEFAULT_DRAW_LAYER)!=None:
    #  self.layer = self.mapContext.getGraphicsLayer(self.DEFAULT_DRAW_LAYER)
    #  self.store = self.layer.getFeatureStore()
    #  print "alredy has", self.layer
    #else:
    self.store = createMemoryStore()
    self.layer = DrawGraphicLayer()
    self.layer.setDataStore(self.store)
    self.mapContext.setGraphicsLayer(self.DEFAULT_DRAW_LAYER, self.layer)

    #DELETE
    self.layer.setName("TESTING QUICK")
    gvsig.currentView().addLayer(self.layer)
    
    
  def initUI(self):
    tsl = ToolsSwingLocator.getToolsSwingManager()
    self.jslOutline.setPaintLabels(False)
    self.jslFill.setPaintLabels(False)
    self.pickerColorOutline = tsl.createColorPickerController(self.txtOutline, self.btnOutline, self.jslOutline)
    self.pickerColorFill = tsl.createColorPickerController(self.txtFill, self.btnFill, self.jslFill)
    
  def btnDrawPoint_click(self, *args):
    quickdrawingpoint = QuickDrawingPoint()
    quickdrawingpoint.setTool(self.mapControl)
    
  def btnDrawPolyline_click(self, *args):
    quickdrawingpolyline = QuickDrawingPolyline()
    print "selfstore:", self.store
    quickdrawingpolyline.setStore(self.store)
    quickdrawingpolyline.setTool(self.mapControl)
    
  
def main(*args):
  
  p = QuickDrawingTool()
  p.showTool("QuickDrawing")
