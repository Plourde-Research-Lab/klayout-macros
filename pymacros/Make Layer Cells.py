# $description: Split into layer cells
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
        
        
def make_layer_cells():

    #Load View
    app = pya.Application.instance()
    mw = app.main_window()
    lv = mw.current_view()
    ly = lv.active_cellview().layout()
    dbu = ly.dbu
    
    if lv==None:
        raise Exception("No view selected")
        
    cv = lv.cellview(lv.active_cellview_index())
    
    #Loop through layers
    
    for layer in [1,2,3]:
      new_cell = ly.create_cell(cv.cell.display_title() + "L" + str(layer))
      
      # Loop through instances
      for inst in cv.cell.each_inst():
       
       #Calculate location of instances
        itrans = pya.ICplxTrans.from_trans(pya.CplxTrans())
        box = inst.bbox().transformed(itrans)
        x = box.center().x
        y = box.center().y

        #Create new cell to represent given layer
        new_subcell = ly.create_cell(inst.cell.display_title() + "L" + str(layer))
        
        #Map Bounding box and shape layers to new layer
        lm = pya.LayerMapping()
        lm.map(ly.layer(1,3), ly.layer(1,3))
        lm.map(ly.layer(layer, 0), ly.layer(layer, 0))
        lm.map(ly.layer(layer,1), ly.layer(layer, 0))
        
        #Create Instance Array to place into cell
        array = pya.CellInstArray()
        
        #Copy shapes, place, and insert
        array.cell_index=new_subcell.cell_index()
        new_subcell.copy_shapes(inst.cell, lm)
        array.trans = pya.Trans(pya.Point(x,y))
        new_cell.insert(array)
      

x = MenuAction("Make Layer Cells", "", make_layer_cells)

app = pya.Application.instance()
mw = app.main_window()
menu = mw.menu()
menu.insert_separator("@hcp_context_menu.end", "sep_layer_cells")
menu.insert_item("@hcp_context_menu.end", "layer_cells", x)