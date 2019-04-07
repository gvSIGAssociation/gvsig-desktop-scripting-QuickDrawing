# encoding: utf-8

import gvsig

from gvsig import getResource
from gvsig.libs.formpanel import FormPanel
from addons.QuickDrawing.qdlib.qdpoint import QuickDrawingPoint
from org.gvsig.tools.swing.api import ToolsSwingLocator


class QuickDrawingTool(FormPanel):
  def __init__(self):
    FormPanel.__init__(self,getResource(__file__,"quickDrawingTool.xml"))
    self.initUI()
  def initUI(self):
    tsl = ToolsSwingLocator.getToolsSwingManager()
    self.jslOutline.setPaintLabels(False)
    self.jslFill.setPaintLabels(False)
    pickerColorOutline = tsl.createColorPickerController(self.txtOutline, self.btnOutline, self.jslOutline)
    pickerColorFill = tsl.createColorPickerController(self.txtFill, self.btnFill, self.jslFill)
    
  def btnDrawPoint_click(self, *args):
    print "print"
    viewDoc = gvsig.currentView()
    viewPanel = viewDoc.getWindowOfView()
    mapControl = viewPanel.getMapControl()
    print "t1:", type(viewDoc)
    print "t2:", type(viewPanel)
    print "t3:", type(mapControl)
    
    quickdrawingpoint = QuickDrawingPoint()
    quickdrawingpoint.setTool(mapControl)
  
def main(*args):
  p = QuickDrawingTool()
  p.showTool("QuickDrawing")
