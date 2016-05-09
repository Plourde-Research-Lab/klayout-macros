# $description: Make CPW out of Path
# $autorun
# $show-in-menu
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

def make_cpw():

    #Load View
    app = pya.Application.instance()
    mw = app.main_window()
    lv = mw.current_view()
    ly = lv.active_cellview().layout()
    dbu = ly.dbu
    
    center_radius = 100.0/dbu #Curve radius
    center_width = 10./dbu #Center conductor width
    s_width = 6./dbu #Center - Outer conductor spacing
    keepout_width = 4./dbu #Keepout spacing
    
    ri = center_radius - .5*center_width #Inner radius
    ro = center_radius + .5*center_width # Outer radius
    n = 10/dbu #Number of points per curve
    
    cpw_layer = ly.layer(1,0)
    keepout_layer = ly.layer(1,6)
    
    if lv==None:
        raise Exception("No view selected")
    
    lv.transaction("Make CPW")
    
    selected_objects = lv.each_object_selected()
    print("x")
    for obj in selected_objects:
        if obj.shape.is_path() and not obj.is_cell_inst():
            inner = pya.Path()
            outer = pya.Path()
            keepout = pya.Path()
            print(obj.shape.path)
            
            inner = obj.shape.path
            outer = obj.shape.path
            keepout = obj.shape.path
            
            #Adjust widths
            inner.width = center_width
            outer.width = inner.width + 2*s_width
            keepout.width = outer.width + 2*keepout_width
            
            #Round Corners
            inner = [inner.polygon().round_corners(ri, ro, n)]
            outer = [outer.polygon().round_corners(ri-s_width,ro+s_width, n)]
            keepout = keepout.polygon().round_corners(ri-s_width-keepout_width, ro+s_width+keepout_width, n)
            
            #Subtract inner from outer
            ep = pya.EdgeProcessor()
            outer_minus_inner = ep.boolean_p2p(outer, inner, pya.EdgeProcessor().ModeANotB, True, False)
            
            for p in outer_minus_inner:
                lv.active_cellview().cell.shapes(cpw_layer).insert(p)
            
           # lv.active_cellview().cell.shapes(cpw_layer).insert(outer_minus_inner[0])
            lv.active_cellview().cell.shapes(keepout_layer).insert(keepout)
            
    lv.commit()
    
    #pya.MessageBox.info("Test", "It worked bitches", pya.MessageBox.b_ok())
    
x = MenuAction("Make CPW", "", make_cpw)

app = pya.Application.instance()
mw = app.main_window()
menu = mw.menu()
menu.insert_separator("tools_menu.end", "sep_cpw")
menu.insert_item("tools_menu.end", "cpw", x)