# $description: Run Shapes in FastHenry
# $autorun
# $show-in-menu
import pya
import sys
import types
from os.path import curdir, join
from fasthenry import *

sys.stderr = sys.stdout


class MenuAction(pya.Action):
    def __init__(self, title, shortcut, action):
        self.title = title
        self.shortcut = shortcut
        self.action = action

    def triggered(self):
        self.action()
        
def writeInputFile(self, clicked):
    global fh
    lv = pya.Application.instance().main_window().current_view()
    selected_objects = lv.each_object_selected()
    ly = lv.active_cellview().layout()
    dbu = ly.dbu
    # Take Inputs
    nwincInput = self.nwincInput.text
    nhincInput = self.nhincInput.text
    startFreq = self.startFreqInput.text
    stopFreq = self.stopFreqInput.text
    numPts = self.ptsInput.text
    
    fh = FastHenryFile(nwinc=nwincInput, nhinc=nhincInput, pen_depth=85e-3,
                                start_freq=startFreq, stop_freq=stopFreq, numpts=numPts)
    for obj in selected_objects:
        if obj.shape().is_path() and not obj.is_cell_inst():
            pts = []
            pth = obj.shape().path
            # create point object for each point
            for i, pt in enumerate(pth.each_point()):
                p = point(obj.shape().property('1') + str(i),
                          float(pt.x*dbu),
                          float(pt.y*dbu))
                pts.append(p)
            # create shape
            sh = shape(obj.shape().property('1'), pts, width=pth.width*dbu)
            fh.shapes.append(sh)
    
    self.inputFilePreview.setText(str(fh))
    
    # Write file and call fasthenry
    fh.print_to_file()
    
def callFastHenry(self, clicked):
    global fh
    out, result = fh.call_fh()
    # Display Results
    self.outputPreview.setText(result)

def runInFastHenry():

    # Load View
    app = pya.Application.instance()
    mw = app.main_window()
    lv = mw.current_view()
    ly = lv.active_cellview().layout()
    dbu = ly.dbu
    
    # Setup GUI
    ui_path = join("C:\\Users\Caleb\Development\klayout-macros\pymacros", "FastHenryGui.ui") 
 
    ui_file = pya.QFile(ui_path)
    parent = pya.Application.instance().main_window()
    ui_file.open(pya.QIODevice.ReadOnly)
    form = pya.QFormBuilder().load(ui_file, parent)
    ui_file.close()
    
    # Bind Functions
    form.writeInputBtn.clicked(types.MethodType(writeInputFile, form))
    form.runBtn.clicked(types.MethodType(callFastHenry, form))

    # Load Shapes
    if lv is None:
        raise Exception("No view selected")

    selected_objects = lv.each_object_selected()
    for obj in selected_objects:
        if obj.shape().is_path() and not obj.is_cell_inst():
            form.traceComboBox.addItem(obj.shape().property('1'))
    
    form.exec_()

# Declare fh object globally, so different functions can access
fh = []

# Add to Menu
x = MenuAction("Run in FastHenry", "", runInFastHenry)
app = pya.Application.instance()
mw = app.main_window()
menu = mw.menu()
menu.insert_separator("tools_menu.end", "sep_fh")
menu.insert_item("tools_menu.end", "fh", x)
