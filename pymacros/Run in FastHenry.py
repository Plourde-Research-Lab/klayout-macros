# $description: Run Shapes in FastHenry
# $autorun
# $show-in-menu
import pya
import sys
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


def runInFastHenry():

    # Load View
    app = pya.Application.instance()
    mw = app.main_window()
    lv = mw.current_view()
    ly = lv.active_cellview().layout()
    dbu = ly.dbu

    if lv is None:
        raise Exception("No view selected")

    selected_objects = lv.each_object_selected()

    fh = FastHenryFile()
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
            sh = shape(obj.shape().property('1'), pts)
            fh.shapes.append(sh)

    # Write file and call fasthenry
    fh.print_to_file()
    out, result = fh.call_fh()
    # D isplay Results
    pya.MessageBox.info("FastHenry", result, pya.MessageBox.b_ok())


x = MenuAction("Run in FastHenry", "", runInFastHenry)
app = pya.Application.instance()
mw = app.main_window()
menu = mw.menu()
menu.insert_separator("tools_menu.end", "sep_fh")
menu.insert_item("tools_menu.end", "fh", x)
