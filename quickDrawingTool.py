# encoding: utf-8

import gvsig

from gvsig import getResource
from gvsig.libs.formpanel import FormPanel

from qdlib.qdpoint import QuickDrawingPoint
from qdlib.qdpolyline import QuickDrawingPolyline
from qdlib.drawGraphicLayer import createMemoryStore
from qdlib.qdselect import QuickDrawingSelect
from qdlib.qdpolylineclosed import QuickDrawingPolylineClosed
from qdlib.qdpolygon import QuickDrawingPolygon
from qdlib.qdcircle import QuickDrawingCircle
from qdlib.qdcircumference import QuickDrawingCircumference
from qdlib.qdellipse import QuickDrawingEllipse
from qdlib.qdellipsefill import QuickDrawingEllipseLine
from qdlib.qdselectrectangle import QuickDrawingSelectRectangle
from qdlib.qdrectangle import QuickDrawingRectangle
from qdlib.qdfreehand import QuickDrawingFreehand

from java.awt import Color
from org.gvsig.tools.swing.api import ToolsSwingLocator
from org.gvsig.fmap.mapcontext import MapContextLocator
from org.gvsig.gui.beans.swing import JComboBoxFonts
from org.gvsig.symbology.fmap.mapcontext.rendering.legend.styling import LabelingFactory

class QuickDrawingTool(FormPanel):
  DEFAULT_DRAW_LAYER = 'DrawGraphicsLayer'
  def __init__(self):
    FormPanel.__init__(self,getResource(__file__,"quickDrawingTool2.xml"))
    self.initUI()
    self.mapContext = gvsig.currentView().getMapContext()
    self.mapControl = gvsig.currentView().getWindowOfView().getMapControl()
    if self.mapContext.getGraphicsLayer(self.DEFAULT_DRAW_LAYER)!=None:
      self.layer = self.mapContext.getGraphicsLayer(self.DEFAULT_DRAW_LAYER)
      self.store = self.layer.getFeatureStore()
    else:
      self.store = createMemoryStore()
      mapContextManager = MapContextLocator.getMapContextManager()
      self.layer = mapContextManager.createLayer(self.DEFAULT_DRAW_LAYER,self.store)
      self.mapContext.setGraphicsLayer(self.DEFAULT_DRAW_LAYER, self.layer)

    #DELETE
    
    #self.layer.setName(DEFAULT_DRAW_LAYER)
    #print "layer to add: ", self.layer
    
    #gvsig.currentView().addLayer(self.layer)
        ## Apply legend
    
    from org.gvsig.symbology import SymbologyLocator
    m = SymbologyLocator.getSymbologyManager()
    vl = m.createDynamicVectorLegend()
    
    self.layer.setLegend(vl)
    

    dynamicLabeling = LabelingFactory.createDynamicLabelingStrategy()
    self.layer.setLabelingStrategy(dynamicLabeling)
    self.layer.setIsLabeled(True)

  def getGraphicLayer(self):
    return self.layer
    
  def initUI(self):
    tsl = ToolsSwingLocator.getToolsSwingManager()
    self.jslOutline.setPaintLabels(False)
    self.jslFill.setPaintLabels(False)
    self.jslLabelColor.setPaintLabels(False)
    self.pickerColorOutline = tsl.createColorPickerController(self.txtOutline, self.btnOutline, self.jslOutline)
    self.pickerColorFill = tsl.createColorPickerController(self.txtFill, self.btnFill, self.jslFill)
    self.spnWidth.setValue(1)
    self.cfonts = JComboBoxFonts()
    try:
      self.cfonts.setSelectedItem("DejaVu Sans")
      self.cfonts.setSelectedItem("Liberation Sans")
      self.cfonts.setSelectedItem("Serif")
      self.cfonts.setSelectedItem("Arial")
    except:
      pass
    self.jpn1.add(self.cfonts)
    self.jpn1.updateUI()

    self.spnLabelSize.setValue(12)
    self.pickerFontColor = tsl.createColorPickerController(self.txtLabelColor, self.btnLabelColor, self.jslLabelColor)

    
  def btnDrawPoint_click(self, *args):
    quickdrawingpoint = QuickDrawingPoint()
    quickdrawingpoint.setUI(self)
    quickdrawingpoint.setLayer(self.layer)
    quickdrawingpoint.setTool(self.mapControl)
    
  def btnDrawSelect_click(self, *args):
    quickdrawingselect = QuickDrawingSelect()
    quickdrawingselect.setUI(self)
    quickdrawingselect.setLayer(self.layer)
    quickdrawingselect.setTool(self.mapControl)
    
  def btnDrawSelectRectangle_click(self, *args):
    quickdrawingselectrectangle = QuickDrawingSelectRectangle()
    quickdrawingselectrectangle.setUI(self)
    quickdrawingselectrectangle.setLayer(self.layer)
    quickdrawingselectrectangle.setTool(self.mapControl)
    
  def btnDrawPolyline_click(self, *args):
    quickdrawingpolyline = QuickDrawingPolyline()
    quickdrawingpolyline.setUI(self)
    quickdrawingpolyline.setLayer(self.layer)
    quickdrawingpolyline.setTool(self.mapControl)
    
  def btnDrawPolylineClosed_click(self, *args):
    quickdrawingpolyline = QuickDrawingPolylineClosed()
    quickdrawingpolyline.setUI(self)
    quickdrawingpolyline.setLayer(self.layer)
    quickdrawingpolyline.setTool(self.mapControl)
    
  def btnDrawPolygon_click(self, *args):
    quickdrawingpolyline = QuickDrawingPolygon()
    quickdrawingpolyline.setUI(self)
    quickdrawingpolyline.setLayer(self.layer)
    quickdrawingpolyline.setTool(self.mapControl)
    
  def btnDrawCircle_click(self, *args):
    quickdrawingcircle = QuickDrawingCircle()
    quickdrawingcircle.setUI(self)
    quickdrawingcircle.setLayer(self.layer)
    quickdrawingcircle.setTool(self.mapControl)
    
  def btnDrawCircumference_click(self, *args):
    quickdrawingcircumference = QuickDrawingCircumference()
    quickdrawingcircumference.setUI(self)
    quickdrawingcircumference.setLayer(self.layer)
    quickdrawingcircumference.setTool(self.mapControl)
    
  def btnDrawEllipse_click(self, *args):
    quickdrawingellipse = QuickDrawingEllipse()
    quickdrawingellipse.setUI(self)
    quickdrawingellipse.setLayer(self.layer)
    quickdrawingellipse.setTool(self.mapControl)
    
  def btnDrawEllipseLine_click(self, *args):
    quickdrawingellipsefill = QuickDrawingEllipseLine()
    quickdrawingellipsefill.setUI(self)
    quickdrawingellipsefill.setLayer(self.layer)
    quickdrawingellipsefill.setTool(self.mapControl)
    
  def btnDrawRectangle_click(self, *args):
    quickdrawrectangle = QuickDrawingRectangle()
    quickdrawrectangle.setUI(self)
    quickdrawrectangle.setLayer(self.layer)
    quickdrawrectangle.setTool(self.mapControl)
    
  def btnDrawHand_click(self, *args):
    quickdrawingfreehand = QuickDrawingFreehand()
    quickdrawingfreehand.setUI(self)
    quickdrawingfreehand.setLayer(self.layer)
    quickdrawingfreehand.setTool(self.mapControl)
    
  def btnDrawDelete_click(self, *args):
    if not self.store.isEditing():
      self.store.edit()
    features = self.store.getFeatureSelection()
    for f in features:
      features.delete(f)
    #self.store.commit()
    self.mapContext.invalidate()
    pass
    
  def btnApply_click(self, *args):
    values = self.graphicValues()
    if not self.store.isEditing():
      self.store.edit()
    features = self.store.getFeatureSelection()
    for f in features:
      fe = f.getEditable()
      for key,value in values.iteritems():
        fe.set(key, value)
      self.store.update(fe)
    #self.store.commit()
    self.mapContext.invalidate()
    print "end apply"
    
  def graphicValues(self):
    values = {"COUTLINE": self.pickerColorOutline.get().getRGB(),
              "CFILL": self.pickerColorFill.get().getRGB(),
              "CSIZE": self.spnWidth.getValue(),
              "CROTATION": self.spnRotation.getValue(),
              "LTEXT": "'"+self.txtLabelText.getText()+"'",
              "LCOLOR": self.pickerFontColor.get().getRGB(),
              "LROTATION":self.spnLabelRotation.getValue(),
              "LFONT": "'"+self.cfonts.getSelectedItem()+"'",
              "LFONTS": 0,
              "LHEIGHT": self.spnLabelSize.getValue()
              }
    return values
    
  def setUIValues(self, values):
    outline = Color(values["COUTLINE"], True)
    self.pickerColorOutline.set(outline)
    
    fill = Color(values["CFILL"], True)
    self.pickerColorFill.set(fill)
    
    size = values["CSIZE"]
    self.spnWidth.setValue(size)
    
    rotation = values["CROTATION"]
    self.spnRotation.setValue(rotation)
    
    ltext = values["LTEXT"].replace("'","")
    self.txtLabelText.setText(ltext)
    
    lcolor = Color(values["LCOLOR"], True)
    self.pickerFontColor.set(lcolor)
    
    lrotation = values["LROTATION"]
    self.spnLabelRotation.setValue(lrotation)
    
    lfont = values["LFONT"].replace("'","")
    print lfont
    try:
      self.cfonts.setSelectedItem(lfont)
    except:
      pass
    
    lfonts = values["LFONTS"]
    
    lheight = values["LHEIGHT"]
    self.spnLabelSize.setValue(lheight)
    
  
def main(*args):
  
  p = QuickDrawingTool()
  p.showTool("QuickDrawing")
  print "values:", p.graphicValues()
