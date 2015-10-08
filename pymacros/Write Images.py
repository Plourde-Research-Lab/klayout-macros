# $description: Write Image Distribution from Wafer
# $autorun
# $show-in-menu
import pya
import sys
from math import copysign
from numpy import arange

sys.stderr = sys.stdout

class MenuAction(pya.Action):
    def __init__(self, title, shortcut, action):
        self.title = title
        self.shortcut = shortcut
        self.action = action
        
    def triggered(self):
        self.action()
        
        
def write_distribution(job_file, cv, dbu):

  #For cellinstarray in wafer
  #Loop through various layouts on wafer
  
  #For cellinst in cellinstarray
  #Loop through all dies in particular layout, (cell selection)
  
  #For images in cellinst
  #Loop through images in die, writing entry for each image
  
  for inst in cv.cell.each_inst():
    subcell = inst.cell
    
    
    # Determine indexes for cell selection
    if copysign(1, inst.a.x) == 1:
      start_index_x = 0
    else:
      start_index_x = 1
      
    if copysign(1, inst.b.y) == 1:
      start_index_y = 0
    else:
      start_index_y = 1
      
    x_index = arange(copysign(start_index_x, inst.a.x), copysign(inst.na, inst.a.x) + copysign(start_index_x, inst.a.x), copysign(1, inst.a.x))
    y_index = arange(copysign(start_index_y, inst.b.y), copysign(inst.nb, inst.b.y) + copysign(start_index_y, inst.b.y), copysign(1, inst.b.y))
    
    # Write each die type
    print("\nPrinting {} dies containing {}".format(inst.na*inst.nb, subcell.basic_name()))
    for i in x_index:
      for j in y_index:
        print("\tPrinting die at {:.0f}, {:.0f}".format(i, j))
        for image in subcell.each_inst():
          
          #Get position
          itrans = pya.ICplxTrans.from_trans(pya.CplxTrans())
          box = image.bbox().transformed(itrans)
          x = box.center().x*dbu/1000.
          y = box.center().y*dbu/1000.
          
          #Write definition
          text = 'START_SECTION IMAGE_DISTRIBUTION\n'
          text += '\tIMAGE_ID                                         "{}"\n'.format(image.cell.basic_name())
          text += '\tINSTANCE_ID                                   "{}"\n'.format("<Default>")
          text += '\tCELL_SELECTION                             "{:.0f}" "{:.0f}"\n'.format(i, j)
          text += '\tDISTRIBUTION_ACTION                  "I"\n'
          text += '\tOPTIMIZE_ROUTE                            "N"\n'
          text += '\tIMAGE_CELL_SHIFT                          {:.06f} {:.06f}\n'.format(x, y)
          text += 'END_SECTION\n\n'
          print(text)
          job_file.write(text)

    #for image in subcell.each_inst():
      #print(image.cell.basic_name())

  '''text = 'START_SECTION IMAGE_DISTRIBUTION\n'
  text += '\tIMAGE_ID                                      "{}"\n'.format()
  text += '\tINSTANCE_ID                                   "{}"\n'.format()
  text += '\tCELL_SELECTION                                "{}" "{}"\n'.format()
  text += '\tDISTRIBUTION_ACTION                           "I"\n'
  text += '\tOPTIMIZE_ROUTE                                "N"\n'
  text += '\tIMAGE_CELL_SHIFT                              {} {}\n'.format()
  text += 'END_SECTION\n\n'
'''
def write_images():
  
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
  if (cv.cell.name.lower() != "wafer"):
    raise "Make your \"Wafer\" cell your current view."
  
  if not cv.is_valid():
    raise "No layout selected"
    
  #Get parameters
  filename = pya.FileDialog.ask_save_file_name("ASML Job file", "test.asml", "ASML files (*.asml *.txt)")

  if filename:
    job_file = open(filename, 'a')
    #Print image distribution
    
    write_distribution(job_file, cv, dbu)

    #Print layer definition
    
    #Print process data
    
    #Print reticle data
    job_file.close()
    
    

x = MenuAction("Write Image Distribution", "", write_images)

app = pya.Application.instance()
mw = app.main_window()
menu = mw.menu()
menu.insert_separator("@hcp_context_menu.end", "sep_write_images")
menu.insert_item("@hcp_context_menu.end", "write_images", x)