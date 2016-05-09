# $autorun
# $show-in-menu
# Calc freq

from cpw_design import cpw

import pya
import sys
sys.stderr = sys.stdout

class MenuAction(pya.Action):
    def __init__(self, title, shortcut, action):
        self.title = title
        self.shortcut = shortcut
        self.action = action
        
    def triggered(self):
        self.action()

def calc_freq():

    #Load View
    app = pya.Application.instance()
    mw = app.main_window()
    lv = mw.current_view()
    ly = lv.active_cellview().layout()
    dbu = ly.dbu
    
    
    if lv==None:
        raise Exception("No view selected")
        
    total_length = 0.0

    #CPW consists of  6um wide polygons
    cpw_width = 10.0
    
    #Difference in length after rounding corners
    delta_r = 42.29
    
    lv.transaction("Calculate Frequency")
    
    selected_objects = lv.each_object_selected()
    
    for obj in selected_objects:
        if obj.shape.is_path() and not obj.is_cell_inst():
          shape = obj.shape
          polygon = shape.polygon
          a = polygon.area()
          m = obj.trans().mag * ly.dbu
          total_length += a * m * m / cpw_width
          
          #subtract difference from rounding corners
          total_length -= (shape.path.num_points()-2)*delta_r
          
    
    freq = str(cpw(l=total_length).fn()*1e-9) + " GHz"
    pya.MessageBox().info("Frequency", freq, pya.MessageBox().b_ok())


x = MenuAction("Calculate Frequency", "", calc_freq)

app = pya.Application.instance()
mw = app.main_window()
menu = mw.menu()
menu.insert_separator("tools_menu.end", "sep_freq")
menu.insert_item("tools_menu.end", "freq", x)