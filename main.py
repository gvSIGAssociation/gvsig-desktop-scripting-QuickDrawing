# encoding: utf-8

import gvsig

from gvsig import getResource
from gvsig.libs.formpanel import FormPanel

class ToolQuickDrawing(FormPanel):
  def __init__(self):
    FormPanel.__init__(self,getResource(__file__,"main.xml"))

def main(*args):
  p = ToolQuickDrawing()
  p.showTool("QuickDrawing")
