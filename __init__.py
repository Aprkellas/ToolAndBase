from vcApplication import *

def OnStart():
  cmduri = getApplicationPath() + 'ToolAndBase.py'
  cmd = loadCommand('ToolAndBase',cmduri)
  addMenuItem('VcTabTeach/Generate', "ToolAndBase", -1, "ToolAndBase")
