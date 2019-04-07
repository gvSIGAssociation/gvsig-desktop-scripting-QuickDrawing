# encoding: utf-8

import gvsig

from gvsig import getResource
from gvsig.libs.formpanel import FormPanel
from addons.QuickDrawing.qdlib.qdpoint import QuickDrawingPoint

class QuickDrawingTool(FormPanel):
  def __init__(self):
    FormPanel.__init__(self,getResource(__file__,"quickDrawingTool.xml"))
    
  def btnDrawPoint_click(*args):
    print "print"
    viewDoc = gvsig.currentView()
    viewPanel = viewDoc.getWindowOfView()
    mapControl = viewPanel.getMapControl()
    
    quickdrawingpoint = QuickDrawingPoint()
    quickdrawingpoint.setTool(mapControl)
  
def main(*args):
  p = QuickDrawingTool()
  p.showTool("QuickDrawing")
