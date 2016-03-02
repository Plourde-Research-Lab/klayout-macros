import time
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
        self.path = join(abspath(curdir), self.filename)
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
        print('Printing {}..\n'.format(self.filename))
        with open(self.filename, 'w') as f:
            f.write(str(self))
        print("Done\n")

    def call_fh(self):
        print(self.path)
        out = subprocess.check_output(['fasthenry.exe', self.path])
        f = open('Zc.mat', 'r')
        result = f.read()
        return out, result
