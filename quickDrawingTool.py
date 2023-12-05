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
from qdlib.qdellipsefill import QuickDrawingEllipseFill
from qdlib.qdselectrectangle import QuickDrawingSelectRectangle
from qdlib.qdrectangle import QuickDrawingRectangle
from qdlib.qdrectanglefill import QuickDrawingRectangleFill
from qdlib.qdfreehand import QuickDrawingFreehand

from java.awt import Color
from org.gvsig.tools.swing.api import ToolsSwingLocator
from org.gvsig.fmap.mapcontext import MapContextLocator
from org.gvsig.gui.beans.swing import JComboBoxFonts
from org.gvsig.symbology.fmap.mapcontext.rendering.legend.styling import LabelingFactory
from org.gvsig.app.gui.styling import JComboBoxUnitsReferenceSystem
from org.gvsig.app.gui import JComboBoxUnits
from org.gvsig.symbology import SymbologyLocator
from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator
from org.gvsig.tools import ToolsLocator
from org.gvsig.tools.persistence import Persistent
from gvsig import logger
from gvsig import LOGGER_WARN,LOGGER_INFO,LOGGER_ERROR
from org.gvsig.fmap.mapcontext.layers.vectorial import FLyrVect
from addons.QuickDrawing import saveloadlayers
from gvsig.geom import *
from java.awt import Font
from org.gvsig.symbology.fmap.mapcontext.rendering.dynamiclegend import DynamicSymbol, DynamicLabelingStrategy, DynamicVectorLegend
from java.awt import BorderLayout

DEFAULT_DRAW_LAYER = 'Free drawing layer'

class QuickDrawingState(Persistent):
  def __init__(self):
      self.layer = None
      self.COUTLINE= 16724787
      self.CFILL = 1701209855
      self.CSIZE=2
      self.CROTATION= 0
      self.LTEXT= ""
      self.LCOLOR=-983144705
      self.LROTATION=0
      self.LFONT=None
      self.LFONTS=0
      self.LHEIGHT=10
      self.LUNIT=11
      self.LREF=1
      self.intoc = False
  def getUIValuesFromState(self):
      values = { 
          "COUTLINE": self.COUTLINE,
          "CFILL": self.CFILL,
          "CSIZE": self.CSIZE,
          "CROTATION": self.CROTATION,
          "LTEXT": self.LTEXT,
          "LCOLOR": self.LCOLOR,
          "LROTATION": self.LROTATION,
          "LFONT":self.LFONT,
          "LFONTS":self.LFONTS,
          "LHEIGHT":self.LHEIGHT,
          "LUNIT":self.LUNIT,
          "LREF":self.LREF
      }
      return values
  def loadFromState(self, state):
      stringlayer = state.getString("graphiclayer")
      
      if stringlayer == None or stringlayer =="":
        return
      else:
        try:
          self.layer = saveloadlayers.loadLayersGraphics(stringlayer)
          self.setDynmicSymbologyLabeling(self.layer)
        except:
          logger("Not been able to load graphic layer from properties: " + stringlayer, LOGGER_WARN)
      # state of the ui
      self.COUTLINE = state.getInt("COUTLINE")
      self.CFILL = state.getInt("CFILL")
      self.CSIZE=  state.getInt("CSIZE")
      self.CROTATION=  state.getInt("CROTATION")
      self.LTEXT=  state.getString("LTEXT")
      self.LCOLOR=  state.getInt("LCOLOR")
      self.LROTATION=  state.getInt("LROTATION")
      self.LFONT= state.get("LFONT")
      self.LFONTS= state.getInt("LFONTS")
      self.LHEIGHT= state.getInt("LHEIGHT")
      self.LUNIT= state.getInt("LUNIT")
      self.LREF= state.getInt("LREF")
 
  def saveToState(self, state):
      try:
        layerjson = saveloadlayers.saveGraphicsLayers(self.layer)
      except:
        logger("Not been able to convert graphic layer into json. Layer: "+self.layer, LOGGER_WARN)
      
      state.set("graphiclayer", layerjson)
      
      # ui values
      state.setValue("COUTLINE",self.COUTLINE)
      state.setValue("CFILL",self.CFILL)
      state.setValue("CSIZE",self.CSIZE)
      state.setValue("CROTATION",self.CROTATION)
      state.setValue("LTEXT",self.LTEXT)
      state.setValue("LCOLOR",self.LCOLOR)
      state.setValue("LROTATION",self.LROTATION)
      state.setValue("LFONT",self.LFONT)
      state.setValue("LFONTS",self.LFONTS)
      state.setValue("LHEIGHT",self.LHEIGHT)
      state.setValue("LUNIT",self.LUNIT)
      state.setValue("LREF",self.LREF)
      
  def createLayer(self):
      store = createMemoryStore()
      mapContextManager = MapContextLocator.getMapContextManager()
      self.layer = mapContextManager.createLayer(DEFAULT_DRAW_LAYER,store)
      self.layer.setTemporary(True)
      self.setDynmicSymbologyLabeling(self.layer)

  def setDynmicSymbologyLabeling(self, store):
      mcm = MapContextLocator.getMapContextManager()
      vl = mcm.createLegend(DynamicVectorLegend.NAME)
      expression = ExpressionEvaluatorLocator.getManager().createExpression()
      
      expression.setPhrase("COUTLINE")
      vl.setOutlineColor(expression.clone())
      
      expression.setPhrase("CFILL")
      vl.setFillColor(expression.clone())
      
      expression.setPhrase("CSIZE")
      vl.setSize(expression.clone())
      
      expression.setPhrase("CROTATION")
      vl.setRotation(expression.clone())
      
      self.layer.setLegend(vl)
  
  
      # Set dynamic labeling
  
      sm = SymbologyLocator.getSymbologyManager()
      dynamicLabeling  = sm.createLabelingStrategy(DynamicLabelingStrategy.NAME)
      
      expression = ExpressionEvaluatorLocator.getManager().createExpression()
      
      expression.setPhrase("LROTATION")
      dynamicLabeling.setRotation(expression.clone())
      
      expression.setPhrase("LTEXT")
      dynamicLabeling.setText(expression.clone())
      
      expression.setPhrase("LHEIGHT")
      dynamicLabeling.setHeight(expression.clone())
      
      expression.setPhrase("LCOLOR")
      dynamicLabeling.setColor(expression.clone())
      
      expression.setPhrase("LFONT")
      dynamicLabeling.setFont(expression.clone())
      
      expression.setPhrase("LFONTS")
      dynamicLabeling.setFontStyle(expression.clone())
      
      expression.setPhrase("LUNIT")
      dynamicLabeling.setUnit(expression.clone())
      
      expression.setPhrase("LREF")
      dynamicLabeling.setReferenceSystem(expression.clone())
      
      
      self.layer.setLabelingStrategy(dynamicLabeling)
      self.layer.setIsLabeled(True)
      
def registerQuickDrawingStatePersistence():
    manager = ToolsLocator.getPersistenceManager()
    if (manager.getDefinition("QuickDrawingState") == None):
      definition = manager.addDefinition(QuickDrawingState, "QuickDrawingState", "QuickDrawingState persistence definition", None, None)
      definition.addDynFieldString("graphiclayer").setMandatory(False)
      definition.addDynFieldInt("COUTLINE").setMandatory(False)
      definition.addDynFieldInt("CFILL").setMandatory(False)
      definition.addDynFieldInt("CSIZE").setMandatory(False)
      definition.addDynFieldInt("CROTATION").setMandatory(False)
      definition.addDynFieldString("LTEXT").setMandatory(False)
      definition.addDynFieldInt("LCOLOR").setMandatory(False)
      definition.addDynFieldInt("LROTATION").setMandatory(False)
      definition.addDynFieldString("LFONT").setMandatory(False) #.setClassOfValue(Font)
      definition.addDynFieldInt("LFONTS").setMandatory(False)
      definition.addDynFieldInt("LHEIGHT").setMandatory(False)
      definition.addDynFieldInt("LUNIT").setMandatory(False)
      definition.addDynFieldInt("LREF").setMandatory(False)

from java.awt.event import FocusListener

class QDTFocusListener(FocusListener):
    def __init__(self, ui, view):
      self.ui = ui
      self.view = view
      logger("focus init", LOGGER_WARN)
      
    def focusGained(self, e):
      logger("focus gained", LOGGER_WARN)
      self.ui.setEnabled(True)

    def focusLost(self, e): #FocusEvent
      logger("focus lost", LOGGER_WARN)
      self.ui.setEnabled(False)

from javax.swing.event import ChangeListener
class QDTChangeLister(ChangeListener):
  def __init__(self, ui):
    self.ui = ui
    pass
  def stateChanged(self, e): #changeEvent
    #e, mapControl
    currentTool = e.getSource().getCurrentTool()
    updateButtonsUIAction(self.ui, currentTool)

def updateButtonsUIAction(ui, toolName):
  if ui==None:
    return
  btns = [[ui.btnDrawPoint,"quickdrawingpoint"],
    [ui.btnDrawSelect,"quickdrawingselectpoint"],
    [ui.btnDrawSelectRectangle,"quickdrawingselectrectangle"],
    [ui.btnDrawPolyline,"quickdrawingpolyline"],
    [ui.btnDrawPolylineClosed,"quickdrawingpolylineclosed"],
    [ui.btnDrawPolygon,"quickdrawingpolygon"],
    [ui.btnDrawCircle,"quickdrawingcircle"],
    [ui.btnDrawCircumference,"quickdrawingcircumference"],
    [ui.btnDrawEllipse,"quickdrawingellipse"],
    [ui.btnDrawEllipseFill,"quickdrawingellipsefill"],
    [ui.btnDrawRectangle,"quickdrawingrectangle"],
    [ui.btnDrawRectangleFill,"quickdrawingrectanglefill"],
    [ui.btnDrawHand,"quickdrawingfreehand"]]
  for btn, action in btns:
    if action==toolName:
      btn.setSelected(True)
    else: 
      btn.setSelected(False)
    
class QuickDrawingTool(FormPanel):
  
  def __init__(self):
    FormPanel.__init__(self,getResource(__file__,"quickDrawingTool2.xml"))

    iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()
    self.btnDrawPoint.setIcon(iconTheme.get("insert-point"))

    self.btnDrawSelect.setIcon(iconTheme.get("selection-simple-select"))
    self.btnDrawSelectRectangle.setIcon(iconTheme.get("selection-select-by-rectangle"))
    self.btnDrawPolyline.setIcon(iconTheme.get("insert-polyline"))
    self.btnDrawPolygon.setIcon(iconTheme.get("insert-polygon"))
    self.btnDrawCircle.setIcon(iconTheme.get("insert-circle-cr"))
    self.btnDrawCircumference.setIcon(iconTheme.get("insert-circumference-cr"))
    self.btnDrawEllipse.setIcon(iconTheme.get("insert-ellipse"))
    self.btnDrawEllipseFill.setIcon(iconTheme.get("insert-filled-ellipse"))
    self.btnDrawRectangle.setIcon(iconTheme.get("insert-rectangle"))
    self.btnDrawRectangleFill.setIcon(iconTheme.get("insert-filled-rectangle"))
    self.btnDrawDelete.setIcon(iconTheme.get("common-remove"))

    self.btnDrawPolylineClosed.setIcon(iconTheme.get("quickdrawing-insert-polyline-closed")) # mine
    self.btnDrawHand.setIcon(iconTheme.get("quickdrawing-insert-freehand-line")) # mine
    #self.btnDrawInsertText.setIcon(iconTheme.get("quickdrawing-insert-text")) # mine

    self.view = gvsig.currentView()
    mapContext = self.view.getMapContext()
    envi = mapContext.getViewPort().getEnvelope()
    if envi is None:
      newEnvelope = createEnvelope(pointMin=createPoint2D(0,0),pointMax=createPoint2D(40,10))
       
      mapContext.getViewPort().setEnvelope(newEnvelope)
    self.mapControl = gvsig.currentView().getWindowOfView().getMapControl()
    if self.mapControl!=None:
      changeListener = QDTChangeLister(self)
      self.mapControl.addChangeToolListener(changeListener)
    #print "add focus.."
    #self.asJComponent().addFocusListener(QDTFocusListener(self, self.view))
    # comprobar si es la misma vista
    #print "..end focus"
    
    self.state = self.view.getProperty("quickdrawingstate")
    
    if self.state != None and self.state.layer==None:
      self.state = None
      
    if self.state == None:
      self.state = QuickDrawingState()
      self.state.createLayer()
      self.view.setProperty("quickdrawingstate", self.state)
    drawLayer = mapContext.getGraphicsLayer(DEFAULT_DRAW_LAYER)
    if drawLayer==None:
      self.state.layer.setProjection(mapContext.getProjection())
      mapContext.setGraphicsLayer(DEFAULT_DRAW_LAYER, self.state.layer)
      mapContext.invalidate()
    
    self.translateUI()
    self.initUI()

    uiValuesFromState = self.state.getUIValuesFromState()
    self.setUIValues(uiValuesFromState)
  def tglTOC_click(self, *args):
    #show in toc
    mapContext = self.view.getMapContext()
    flayers = mapContext.getLayers()
    if self.state.intoc:
      flayers.removeLayer(self.state.layer)
      mapContext.setGraphicsLayer(DEFAULT_DRAW_LAYER, self.state.layer)
      self.state.intoc=False
    else:
      mapContext.removeGraphicsLayer(DEFAULT_DRAW_LAYER)
      flayers.addLayer(self.state.layer)
      self.state.intoc=True
    
  def setUIValuesToState(self):
    uiValues = self.graphicValues()
    for key in uiValues.keys():
      if key == "COUTLINE":
        self.state.COUTLINE= uiValues[key]
      if key == "CFILL":
        self.state.CFILL = uiValues[key]
      if key == "CSIZE":
        self.state.CSIZE=uiValues[key]
      if key == "CROTATION":
        self.state.CROTATION= uiValues[key]
      if key == "LTEXT":
        self.state.LTEXT= uiValues[key]
      if key == "LCOLOR":
        self.state.LCOLOR=uiValues[key]
      if key == "LROTATION":
        self.state.LROTATION=uiValues[key]
      if key == "LFONT":
        self.state.LFONT=uiValues[key]
      if key == "LFONTS":
        self.state.LFONTS=uiValues[key]
      if key  == "LHEIGHT":
        self.state.LHEIGHT=uiValues[key]
      if key == "LUNIT":
        self.state.LUNIT=uiValues[key]
      if key == "LREF":
        self.state.LREF=uiValues[key]
  def setEnabled(self, enabled):
    self.asJComponent().setEnabled(enabled)
    
  def translateUI(self):
    i18nManager = ToolsLocator.getI18nManager()

    #self.tltProperties.setText(i18nManager.getTranslation("_Symbol_properties"))
    self.lblOutlineColor.setText(i18nManager.getTranslation("_Outline_color"))
    self.lblFillColor.setText(i18nManager.getTranslation("_Fill_color"))
    self.lblSize.setText(i18nManager.getTranslation("_Size"))
    self.lblRotation.setText(i18nManager.getTranslation("_Rotation"))
    self.lblLabelText.setText(i18nManager.getTranslation("_Text"))
    self.lblLabelColor.setText(i18nManager.getTranslation("_Label_color"))
    self.lblLabelRotation.setText(i18nManager.getTranslation("_Label_rotation"))
    self.lblLabelFont.setText(i18nManager.getTranslation("_Label_font"))
    self.lblLabelSize.setText(i18nManager.getTranslation("_Label_size"))
    self.lblLabelUnit.setText(i18nManager.getTranslation("_Label_unit"))
    self.lblLabelRef.setText(i18nManager.getTranslation("_Label_ref"))
    self.btnApply.setText(i18nManager.getTranslation("_Apply"))
    #self.tltLabel.setText(i18nManager.getTranslation("_Label_properties"))
    self.chbShowLayer.setText(i18nManager.getTranslation("_Show_draw_graphics_layer"))
    self.tglTOC.setText(i18nManager.getTranslation("_Show_in_TOC"))
  
  def chbShowLayer_click(self,*args):
    if self.state.layer!=None:
      self.state.layer.setVisible(self.chbShowLayer.isSelected())
      self.view.getMapContext().invalidate()
    
  def getGraphicLayer(self):
    return self.state.layer
    
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
    self.jpn1.setLayout(BorderLayout(1,1))
    self.jpn1.add(self.cfonts,BorderLayout.CENTER)
    self.jpn1.updateUI()

    self.cunits = JComboBoxUnits()
    self.jpn2.setLayout(BorderLayout(1,1))
    self.jpn2.add(self.cunits,BorderLayout.CENTER)
    self.jpn2.updateUI()

    self.crefsystem = JComboBoxUnitsReferenceSystem()
    self.jpn3.setLayout(BorderLayout(1,1))
    self.jpn3.add(self.crefsystem,BorderLayout.CENTER)
    self.jpn3.updateUI()
    
    self.spnLabelSize.setValue(12)
    self.pickerFontColor = tsl.createColorPickerController(self.txtLabelColor, self.btnLabelColor, self.jslLabelColor)

    if self.state.layer !=None:
      self.chbShowLayer.setSelected(self.state.layer.isVisible())
    
  def btnDrawPoint_click(self, *args):
    self.setUIValuesToState()
    quickdrawingpoint = QuickDrawingPoint()
    quickdrawingpoint.setUI(self)
    quickdrawingpoint.setLayer(self.state.layer)
    quickdrawingpoint.setTool(self.mapControl)
    
  def btnDrawSelect_click(self, *args):
    self.setUIValuesToState()
    quickdrawingselect = QuickDrawingSelect()
    quickdrawingselect.setUI(self)
    quickdrawingselect.setLayer(self.state.layer)
    quickdrawingselect.setTool(self.mapControl)
    
  def btnDrawSelectRectangle_click(self, *args):
    self.setUIValuesToState()
    quickdrawingselectrectangle = QuickDrawingSelectRectangle()
    quickdrawingselectrectangle.setUI(self)
    quickdrawingselectrectangle.setLayer(self.state.layer)
    quickdrawingselectrectangle.setTool(self.mapControl)
    
  def btnDrawPolyline_click(self, *args):
    self.setUIValuesToState()
    quickdrawingpolyline = QuickDrawingPolyline()
    quickdrawingpolyline.setUI(self)
    quickdrawingpolyline.setLayer(self.state.layer)
    quickdrawingpolyline.setTool(self.mapControl)
    
  def btnDrawPolylineClosed_click(self, *args):
    self.setUIValuesToState()
    quickdrawingpolyline = QuickDrawingPolylineClosed()
    quickdrawingpolyline.setUI(self)
    quickdrawingpolyline.setLayer(self.state.layer)
    quickdrawingpolyline.setTool(self.mapControl)
    
  def btnDrawPolygon_click(self, *args):
    self.setUIValuesToState()
    quickdrawingpolyline = QuickDrawingPolygon()
    quickdrawingpolyline.setUI(self)
    quickdrawingpolyline.setLayer(self.state.layer)
    quickdrawingpolyline.setTool(self.mapControl)
    
  def btnDrawCircle_click(self, *args):
    self.setUIValuesToState()
    quickdrawingcircle = QuickDrawingCircle()
    quickdrawingcircle.setUI(self)
    quickdrawingcircle.setLayer(self.state.layer)
    quickdrawingcircle.setTool(self.mapControl)
    
  def btnDrawCircumference_click(self, *args):
    self.setUIValuesToState()
    quickdrawingcircumference = QuickDrawingCircumference()
    quickdrawingcircumference.setUI(self)
    quickdrawingcircumference.setLayer(self.state.layer)
    quickdrawingcircumference.setTool(self.mapControl)
    
  def btnDrawEllipse_click(self, *args):
    self.setUIValuesToState()
    quickdrawingellipse = QuickDrawingEllipse()
    quickdrawingellipse.setUI(self)
    quickdrawingellipse.setLayer(self.state.layer)
    quickdrawingellipse.setTool(self.mapControl)
    
  def btnDrawEllipseFill_click(self, *args):
    self.setUIValuesToState()
    quickdrawingellipsefill = QuickDrawingEllipseFill()
    quickdrawingellipsefill.setUI(self)
    quickdrawingellipsefill.setLayer(self.state.layer)
    quickdrawingellipsefill.setTool(self.mapControl)
    
  def btnDrawRectangle_click(self, *args):
    self.setUIValuesToState()
    quickdrawrectangle = QuickDrawingRectangle()
    quickdrawrectangle.setUI(self)
    quickdrawrectangle.setLayer(self.state.layer)
    quickdrawrectangle.setTool(self.mapControl)
    
  def btnDrawRectangleFill_click(self, *args):
    self.setUIValuesToState()
    quickdrawrectanglefill = QuickDrawingRectangleFill()
    quickdrawrectanglefill.setUI(self)
    quickdrawrectanglefill.setLayer(self.state.layer)
    quickdrawrectanglefill.setTool(self.mapControl)
    
  def btnDrawHand_click(self, *args):
    self.setUIValuesToState()
    quickdrawingfreehand = QuickDrawingFreehand()
    quickdrawingfreehand.setUI(self)
    quickdrawingfreehand.setLayer(self.state.layer)
    quickdrawingfreehand.setTool(self.mapControl)
    
  def btnDrawDelete_click(self, *args):
    self.setUIValuesToState()
    store = self.state.layer.getFeatureStore()
    if not store.isEditing():
      store.edit()
    features = store.getFeatureSelection()
    for f in features:
      features.delete(f)
    self.view.getMapContext().invalidate()
    
  def btnApply_click(self, *args):
    self.setUIValuesToState()
    values = self.graphicValues()
    store = self.state.layer.getFeatureStore()
    if not store.isEditing():
      store.edit()
    features = store.getFeatureSelection()
    for f in features:
      fe = f.getEditable()
      for key,value in values.iteritems():
        fe.set(key, value)
      store.update(fe)
    self.view.getMapContext().invalidate()

    
  def graphicValues(self):
    values = {"COUTLINE": self.pickerColorOutline.get().getRGB(),
              "CFILL": self.pickerColorFill.get().getRGB(),
              "CSIZE": self.spnWidth.getValue(),
              "CROTATION": self.spnRotation.getValue(),
              "LTEXT": self.txtLabelText.getText(),#"'"+self.txtLabelText.getText()+"'",
              "LCOLOR": self.pickerFontColor.get().getRGB(),
              "LROTATION":self.spnLabelRotation.getValue(),
              "LFONT": self.cfonts.getSelectedItem(),#"'"+self.cfonts.getSelectedItem()+"'",
              "LFONTS": 0,
              "LHEIGHT": self.spnLabelSize.getValue(),
              "LUNIT": self.cunits.getSelectedUnitIndex(),
              "LREF": self.crefsystem.getSelectedIndex()
              }
    #print self.pickerColorFill.get().getRGB()
    return values
    
  def setUIValues(self, values):
    outline = Color(values["COUTLINE"], True)
    if outline!=None:
      self.pickerColorOutline.set(outline)
    
    fill = Color(values["CFILL"], True)
    if fill!=None:
      self.pickerColorFill.set(fill)
    
    size = values["CSIZE"]
    if size!=None:
      self.spnWidth.setValue(size)
    
    rotation = values["CROTATION"]
    if rotation!=None:
      self.spnRotation.setValue(rotation)
    
    ltext = values["LTEXT"]
    if ltext!=None:
      self.txtLabelText.setText(ltext)
    
    lcolor = Color(values["LCOLOR"], True)
    if lcolor!=None:
      self.pickerFontColor.set(lcolor)
    
    lrotation = values["LROTATION"]
    if lrotation!=None:
      self.spnLabelRotation.setValue(lrotation)
    
    lfont = values["LFONT"]
    if lfont!=None:

      try:
        self.cfonts.setSelectedItem(lfont)
      except:
        pass
      
    lfonts = values["LFONTS"]
    
    lheight = values["LHEIGHT"]
    if lheight!=None:
      self.spnLabelSize.setValue(lheight)

    lunit = values["LUNIT"]
    if lunit!=None:
      self.cunits.setSelectedUnitIndex(lunit)
    
    lref = values["LREF"]
    if lref!=None:
      self.crefsystem.setSelectedIndex(lref)
    
  def showTool(self, title):
    ui = self.view.getProperty("quickdrawingtoolui")
    if ui==None:
      self.view.setProperty("quickdrawingtoolui", self)
      FormPanel.showTool(self, title+' - ' + self.view.getName())
      return
    if ui.asJComponent().isShowing():
      ui.asJComponent().grabFocus()
      return
    FormPanel.showTool(self, title+' - ' + self.view.getName())
    return
  
def main(*args):

  p = QuickDrawingTool()
  p.showTool("QuickDrawing")
  print p.graphicValues()
