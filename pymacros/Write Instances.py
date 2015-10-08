# $description: Write Instances and Placements to ASML job file
# $autorun
# $show-in-menu
import pya
import sys
from datetime import datetime
sys.stderr = sys.stdout

class MenuAction(pya.Action):
    def __init__(self, title, shortcut, action):
        self.title = title
        self.shortcut = shortcut
        self.action = action
        
    def triggered(self):
        self.action()
        
def print_general(filename):

  cell_width = 8.1
  cell_height = 8.1
  
  job_name = "Si0x Test Wafer"

  text = ""
  text += 'START_SECTION GENERAL\n'
  text += '\tCOMMENT                                       "Job: {}"\n'.format(job_name)
  text += '\t                                               "Generated on {}"\n'.format(datetime.today().strftime("%x %X"))
  text += '\t                                                 "Caleb Howington"\n'
  text += '\tMACHINE_TYPE                                  "PAS5500/300"\n'
  text += '\tRETICLE_SIZE                                  6\n'
  text += '\tWFR_DIAMETER                                  100.000000\n'
  text += '\tWFR_NOTCH                                     "N"\n'
  text += '\tCELL_SIZE                                     {} {}\n'.format(cell_width, cell_height)
  text += '\tROUND_EDGE_CLEARANCE                          1.000000\n'
  text += '\tFLAT_EDGE_CLEARANCE                           0.000000\n'
  text += '\tEDGE_EXCLUSION                                1.000000\n'
  text += '\tCOVER_MODE                                    "W"\n'
  text += '\tNUMBER_DIES                                   3 14\n'
  text += '\tMIN_NUMBER_DIES                               1\n'
  text += '\tPLACEMENT_MODE                                "O"\n'
  text += '\tMATRIX_SHIFT                                  {} {}\n'.format(cell_width/2, cell_height/2)
  text += '\tPREALIGN_METHOD                               "STANDARD"\n'
  text += '\tWAFER_ROTATION                                0.000000\n'
  text += '\tCOMBINE_ZERO_FIRST                            "N"\n'
  text += '\tMATCHING_SET_ID                               "DEFAULT"\n'
  text += 'END_SECTION\n\n'
        
  print(text)
  filename.write(text)
  
  
def print_image_definitions(filename, cv, reticle_id, dbu):

  
  # Scale for Mask, e.g. 4x
  scale = 4
  
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
    
    print(job_file_text)
    filename.write(job_file_text)
    
def write_distribution():

  #For cellinstarray in wafer
  #Loop through various layouts on wafer
  
  #For cellinst in cellinstarray
  #Loop through all dies in particular layout, (cell selection)
  
  #For images in cellinst
  #Loop through images in die, writing entry for each image

  text = 'START_SECTION IMAGE_DISTRIBUTION\n'
  text += '\tIMAGE_ID                                      "{}"\n'.format()
  text += '\tINSTANCE_ID                                   "{}"\n'.format()
  text += '\tCELL_SELECTION                                "{}" "{}"\n'.format()
  text += '\tDISTRIBUTION_ACTION                           "I"\n'
  text += '\tOPTIMIZE_ROUTE                                "N"\n'
  text += '\tIMAGE_CELL_SHIFT                              {} {}\n'.format()
  text += 'END_SECTION\n\n'


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
  if (cv.cell.name.lower() != "mask"):
    raise "Make your \"Mask\" cell your current view."
  
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
    
    

x = MenuAction("Write Instances", "", write_instances)

app = pya.Application.instance()
mw = app.main_window()
menu = mw.menu()
menu.insert_separator("@hcp_context_menu.end", "sep_write_instances")
menu.insert_item("@hcp_context_menu.end", "write_instances", x)
