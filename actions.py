# encoding: utf-8

import gvsig

import os.path

from os.path import join, dirname

from gvsig import currentView
from gvsig import currentLayer

from java.io import File

from org.gvsig.app import ApplicationLocator
from org.gvsig.andami import PluginsLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools.swing.api import ToolsSwingLocator
from org.gvsig.tools import ToolsLocator
from quickDrawingTool import QuickDrawingTool

class QuickDrawingExtension(ScriptingExtension):
  def __init__(self):
    pass
    
  def canQueryByAction(self):
      return True
  
  def isVisible(self, action):
    if currentView()!=None:
      return True
    return False

  def isLayerValid(self, layer):
    return True
    
  def isEnabled(self, action):
    #if not self.isLayerValid(layer):
    #  return False
    if currentView()!=None:
      return True
    return False

  def execute(self,actionCommand, *args):
    actionCommand = actionCommand.lower()
    if actionCommand == "settool-quickdrawing":
      viewPanel = currentView().getWindowOfView()
      mapControl = viewPanel.getMapControl()
      quickdrawing = QuickDrawingTool()
      i18n = ToolsLocator.getI18nManager()
      quickdrawing.showTool(i18n.getTranslation("_Quick_drawing"))
      
def selfRegisterI18n():
  i18nManager = ToolsLocator.getI18nManager()
  i18nManager.addResourceFamily("text",File(gvsig.getResource(__file__,"i18n")))
  
def selfRegister():
  selfRegisterI18n()
  i18n = ToolsLocator.getI18nManager()
  application = ApplicationLocator.getManager()
  actionManager = PluginsLocator.getActionInfoManager()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()

  quickinfo_icon = File(gvsig.getResource(__file__,"images","quickdrawing.png")).toURI().toURL()
  iconTheme.registerDefault("scripting.quickdrawing", "action", "tools-quickdrawing", None, quickinfo_icon)

  quickdrawing_extension = QuickDrawingExtension()
  quickdrawing_action = actionManager.createAction(
    quickdrawing_extension,
    "tools-quickdrawing",   # Action name
    "Quick drawing",   # Text
    "settool-quickdrawing", # Action command
    "tools-quickdrawing",   # Icon name
    None,                # Accelerator
    1009000000,          # Position
    i18n.getTranslation("_Quick_drawing")    # Tooltip
  )
  quickdrawing_action = actionManager.registerAction(quickdrawing_action)

  # Añadimos la entrada "Report by point" en el menu herramientas
  application.addMenu(quickdrawing_action, "tools/"+i18n.getTranslation("_Quick_drawing"))
  # Añadimos el la accion como un boton en la barra de herramientas "Quickinfo".
  #application.addSelectableTool(quickdrawing_action, "QuickDrawing")
  application.addTool(quickdrawing_action, "QuickDrawing")

def main(*args):
  selfRegister()