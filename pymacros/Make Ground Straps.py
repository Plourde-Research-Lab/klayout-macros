# $description: Make Grounding Straps crossing CPW Paths
# $autorun
# $show-in-menu
import pya
import sys
sys.stderr = sys.stdout
import json
from numpy import sqrt, float64, array, nan, isnan

class MenuAction(pya.Action):
    def __init__(self, title, shortcut, action):
        self.title = title
        self.shortcut = shortcut
        self.action = action
        
    def triggered(self):
        self.action()
        
def make_gnd_straps():

    #Load View
    app = pya.Application.instance()
    mw = app.main_window()
    lv = mw.current_view()
    ly = lv.active_cellview().layout()
    dbu = ly.dbu
    
    if lv==None:
        raise Exception("No view selected")
    
    # Ground Strap parameters
    d = 100/dbu #100 um separation
    l = 22/dbu #22 um long
    w = 8/dbu #8um wide
    gs_layer = ly.layer(2,0)
    
    lv.transaction("Make Grounding Straps")
    
    selected_objects = lv.each_object_selected()

    for obj in selected_objects:
        print(obj.shape())
        m = []
        points = []
        strap_points = []
        pts_per_segment = []
        try:
            if obj.shape().is_path() and not obj.is_cell_inst():
                pth = obj.shape().path
                for pt in pth.each_point():
                    points.append(pt)
                for i in range(0, len(points)-1):
                    #Calculate Slope of cpw and calculate perpendicular slope
                    dx = points[i+1].x - points[i].x
                    dy = points[i+1].y - points[i].y
                    m.append(-float64(dx)/float64(dy))
                    
                    #Calculate distance between points
                    dist = sqrt((points[i+1].x - points[i].x)**2 + (points[i+1].y - points[i].y)**2) 
                    di = d
                    x_offset = .5*l/sqrt(1 + m[i]**2)
                    y_offset = .5*m[i]*l/sqrt(1+m[i]**2)
                    #Check for inf slopes
                    if isnan(x_offset):
                        x_offset = l/2
                    if isnan(y_offset):
                        y_offset = l/2
                        
                    while di < dist:
                        new_x = points[i].x + di/dist*(points[i+1].x-points[i].x)
                        new_y = points[i].y + di/dist*(points[i+1].y-points[i].y)
                        firstpt = pya.Point(new_x+x_offset, new_y+y_offset)
                        endpt = pya.Point(new_x-x_offset, new_y-y_offset)
                        strap =pya.Path( [firstpt, endpt], w)
                        lv.active_cellview().cell.shapes(gs_layer).insert(strap)
                        di+=d
                    pts_per_segment.append(di/d)
                    print("Writing {} straps".format(di/d))
                    
        except StopIteration:
            pya.MessageBox.info("Test", "It worked bitches", pya.MessageBox.b_ok())
        
    lv.commit()
    
    #pya.MessageBox.info("Test", "It worked bitches", pya.MessageBox.b_ok())
    
x = MenuAction("Make Ground Straps", "", make_gnd_straps)

app = pya.Application.instance()
mw = app.main_window()
menu = mw.menu()
menu.insert_separator("tools_menu.end", "sep_gnd_straps")
menu.insert_item("tools_menu.end", "gnd_straps", x)