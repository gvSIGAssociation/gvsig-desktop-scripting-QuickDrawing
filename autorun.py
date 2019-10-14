# encoding: utf-8

import gvsig

from addons.QuickDrawing import actions
from org.gvsig.app.project import ProjectManager
from org.gvsig.tools.util.BaseListenerSupport import NotificationListener
from org.gvsig.app.project.ProjectManager import NewProjectEvent
from addons.QuickDrawing import saveloadlayers
from org.gvsig.app.project import ProjectNotification
from org.gvsig.tools.observer import Observer, Notification
from addons.QuickDrawing import quickDrawingTool

def main(*args):
  actions.selfRegister()
  quickDrawingTool.registerQuickDrawingStatePersistence()
  prepareGraphicsLayer()
  
def prepareGraphicsLayer():
  
  #project = currentProject()
  projectManager = ProjectManager.getInstance()
  projectManager.addProjectListener(ProjectManagerListener())
 
class ProjectManagerListener(NotificationListener):
  def __init__(self):
    pass
  def notify(self, event):
    print "Graphics Layer notify: ", event, type(event)
    if isinstance(event, NewProjectEvent):
      event.getProject().addObserver(ProjectObserver())
      #saveloadlayers.saveGraphicsLayers(project)
      #print "-- saved"
                    
    
class ProjectObserver(Observer):
  def update(self, project, notification):
    if not isinstance(notification, Notification):
      return
    if notification == ProjectNotification.BEFORE_SAVE_TO_STATE:
      print "save"
    elif notification == ProjectNotification.AFTER_LOAD_FROM_STATE:
      print "load"
