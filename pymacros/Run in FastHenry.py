# $description: Run Shapes in FastHenry
# $autorun
# $show-in-menu
import pya
import sys
import types
from os.path import curdir, join
import os


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
    i=0
    for obj in selected_objects:
        if obj.shape.is_path() and not obj.is_cell_inst():
          name = obj.shape.property('1')
          if name is None:
             name = str(i)
             i = i+1
          pts = []
          pth = obj.shape.path
            # create point object for each point
          for i, pt in enumerate(pth.each_point()):
                p = point(name + str(i),
                          float(pt.x*dbu),
                          float(pt.y*dbu))
                pts.append(p)
            # create shape
          sh = shape(name, pts, width=pth.width*dbu)
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
    ui_path = join("/Users/caleb/Development/klayout-macros/pymacros", "FastHenryGui.ui") 

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
    i=0
    for obj in selected_objects:
        if obj.shape.is_path() and not obj.is_cell_inst():
            name = obj.shape.property('1')
            if name is None:
              name = str(i)
              i = i+1
            print(name)
            form.traceComboBox.addItem(name)
    
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

import time
#from subprocess import Popen, PIPE
import subprocess
from os.path import join, curdir, abspath


class point:
    def __init__(self, label, x, y, z=0):
        self.label = label
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "N{} x={} y={} z={}\n".format(self.label, self.x, self.y, self.z)


class segment:
    def __init__(self, label, point1, point2, width, height=.1):
        self.label = label
        self.point1 = point1
        self.point2 = point2
        self.width = width
        self.height = height

    def __repr__(self):
        return "E{} N{} N{} w={} h={}\n".format(self.label, self.point1.label,
               self.point2.label, self.width, self.height)


class shape:
    def __init__(self, label, points, width="10", height=.1):
        self.label = label
        self.points = points
        self.segments = []
        self.width = width
        self.height = height

        for i in range(len(points)-1):
            label_str = "{}{}".format(label, i)
            self.segments.append(segment(label_str, points[i], points[i+1], width, height))

    def __repr__(self):
        string = "\n* Shape {}\n".format(self.label)
        for point in self.points:
            string += str(point)
        for seg in self.segments:
            string += str(seg)
        return string


class FastHenryFile():
    def __init__(self, filename='test', comments='', pen_depth=85e-3,
                 units="um", nwinc=10, nhinc=10, start_freq = 1, stop_freq = 1, numpts = 1):
        self.filename = str(filename) + ".inp"
        self.dir = "/Users/caleb/Development/klayout-macros/pymacros"
        self.path = join(self.dir, self.filename)
        self.comments = str(comments)
        self.pen_depth = float(pen_depth)
        self.units = units
        self.nwinc = int(nwinc)
        self.nhinc = int(nhinc)
        self.start_freq = float(start_freq)
        self.stop_freq = float(stop_freq)
        self.numpts = float(numpts)

        # Elements
        self.points = []
        self.segments = []
        self.groundplanes = []
        self.shapes = []
        print(self.path)

    def header(self):
        string = "* {}\n".format(self.filename)
        string += "* Generated on {}\n".format(time.strftime("%X %x"))
        for line in self.comments.splitlines():
            string += "*{}\n".format(line)
        return string

    def footer(self):
        string = "\n* Define Frequency\n"
        string += ".freq fmin={} fmax={} ndec={}\n".format(self.start_freq, self.stop_freq, self.numpts)
        string += ".end"
        return string

    def externals(self):
        string = "\n*------------ Externals  ------------\n"
        for shape in self.shapes:
            string += "\n* {}\n".format(shape.label)
            string += ".external N{} N{}\n".format(shape.points[0].label, shape.points[-1].label)
        return string

    def params(self):
        string = "\n*------------ Params  ------------\n"
        string +=".Units um\n"
        string += "\n.default lambda={}\n\n".format(self.pen_depth)
        string += ".default nwinc={} nhinc={}\n".format(self.nwinc, self.nhinc)
        return string

    def print_shapes(self):
        string = "\n*------------ Shapes  ------------\n"
        for s in self.shapes:
            string += str(s)
        return string

    def __repr__(self):
        string = self.header() + self.params() + self.print_shapes() + self.externals() + self.footer()
        return string

    def print_to_file(self):
        print('Printing {}..\n'.format(self.path))
        with open(self.path, 'w') as f:
            f.write(str(self))
        print("Done\n")

    def call_fh(self):
        print(self.path)
        out = os.popen('cd /Users/caleb/Development/klayout-macros/pymacros && fasthenry test.inp')
        #out = os.popen('ls')
        while 1:
          if out.readline() == "":
            break
          print(out.readline())
        #f = open('Zc.mat', 'r')
        result = out.read()
        return out, result

    def call_fastHenry(self):
      with Popen(["ls", self.path], stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
          print(line)
      f = open(path.join(self.dir, 'Zc.mat'), 'r')
      result = f.read()
      return out, result