# $description: Write Mask Placements to Excel Spreadsheet
# $autorun
# $show-in-menu
import pya
import sys
from datetime import datetime
#import pandas as pd
import numpy as np
sys.stderr = sys.stdout

class MenuAction(pya.Action):
    def __init__(self, title, shortcut, action):
        self.title = title
        self.shortcut = shortcut
        self.action = action
        
    def triggered(self):
        self.action()
        
def print_image_definitions(filename, cv, reticle_id, dbu):

  
  # Scale for Mask, e.g. 4x
  scale = 4
  
  job_sheet_text = "Name,Width,Height,X,Y\n"
  
  #Calculate location of instances
  
  for inst in cv.cell.each_inst():
  
    itrans = pya.ICplxTrans.from_trans(pya.CplxTrans())
    box = inst.bbox().transformed(itrans)
    width = box.width()*dbu*scale/1000
    height = box.height()*dbu*scale/1000
    x = box.center().x*dbu*scale/1000.
    y = box.center().y*dbu*scale/1000.
    
    job_file_text = "START_SECTION IMAGE_DEFINITION\n"
    job_file_text += "\tIMAGE_ID                                      \"{}\"\n".format(inst.cell.basic_name())
    job_file_text += "\tRETICLE_ID                                    \"{}\"\n".format(reticle_id)
    job_file_text += "\tIMAGE_SIZE                                    {:.06f} {:.06f}\n".format(width, height)
    job_file_text += "\tIMAGE_SHIFT                                  {:.06f} {:.06f}\n".format(x, y)
    job_file_text += "\tMASK_SIZE                                      {:.06f} {:.06f}\n".format(width, height)
    job_file_text += "\tMASK_SHIFT                                    {:.06f} {:.06f}\n".format(x, y)
    job_file_text += "\tVARIANT_ID                                    \"\"\n"
    job_file_text += "END_SECTION\n\n"
    
    job_sheet_text += str(inst.cell.basic_name()) + ","
    job_sheet_text += str(width/scale) +  ","
    job_sheet_text += str(height/scale) +  ","
    job_sheet_text += str(x/scale) +  ","
    job_sheet_text += str(y/scale) +  "\n"
    
    print(job_sheet_text)
    filename.write(job_file_text)
    
    
def write_instances():
  
  #Load View
  app = pya.Application.instance()
  mw = app.main_window()
  lv = mw.current_view()
  ly = lv.active_cellview().layout()
  dbu = ly.dbu
  
  if lv==None:
      raise Exception("No view selected")
      
  cv = lv.cellview(lv.active_cellview_index())
  
  # get the current cell view (Make sure you're running this on your mask)
  #if (cv.cell.name.lower() != "mask"):
    #raise "Make your \"Mask\" cell your current view."
  
  if not cv.is_valid():
    raise "No layout selected"
    
  #Get parameters
  reticle_id = pya.InputDialog.get_string("Reticle ID", "Specify the reticle ID", "mask")
  filename = pya.FileDialog.ask_save_file_name("ASML Job file", "test.asml", "ASML files (*.asml *.txt)")

  if filename:
    job_file = open(filename, 'w')
    
    #Print general
    print_general(job_file)
    
    #Print image definitions
    print_image_definitions(job_file, cv, reticle_id, dbu)
    
    #Print image distribution
    
    
    #Print layer definition
    
    #Print process data
    
    #Print reticle data
    job_file.close()
    
    

x = MenuAction("Write Instances to Excel", "", write_instances)

app = pya.Application.instance()
mw = app.main_window()
menu = mw.menu()
menu.insert_separator("@hcp_context_menu.end", "sep_write_instances_to_excel")
menu.insert_item("@hcp_context_menu.end", "write_instances_to_excel", x)
