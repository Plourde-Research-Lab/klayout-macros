import pya
import numpy as np

"""

"""

class CPW(pya.PCellDeclarationHelper):
  """
  The PCell declaration for a CPW based on a path
  """

  def __init__(self):

    # Important: initialize the super class
    super(CPW, self).__init__()

    # declare the parameters
    self.param("l", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("s", self.TypeShape, "", default = pya.DPath(0, 0))
    self.param("w", self.TypeDouble, "Center Conductor width", default = 10)
    self.param("g", self.TypeInt, "Gap Width", default = 6)
    self.param("name", self.TypeString, "Name", default= "cpw")
    # this hidden parameter is used to determine whether the radius has changed
    # or the "s" handle has been moved
    self.param("length", self.TypeDouble, "Length", default=0.0, readonly=True)
    self.param("frequency", self.TypeDouble, "Frequency", default = 0.0, readonly= True)
    self.param("impedance", self.TypeDouble, "Impedance", default = 50., readonly = True)

  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "CPW(L=" + str(self.length) + ",Name=" + str(self.name)")"

  def coerce_parameters_impl(self):

    # We employ coerce_parameters_impl to decide whether the handle or the
    # numeric parameter has changed (by comparing against the effective
    # radius ru) and set ru to the effective radius. We also update the
    # numerical value or the shape, depending on which on has not changed.
    rs = None
    if isinstance(self.s, pya.DPoint):
      # compute distance in micron
      rs = self.s.distance(pya.DPoint(0, 0))
    if rs != None and abs(self.r-self.ru) < 1e-6:
      self.ru = rs
      self.r = rs
    else:
      self.ru = self.r
      self.s = pya.DPoint(-self.r, 0)

    self.rd = 2*self.r

    # n must be larger or equal than 4
    if self.n <= 4:
      self.n = 4

  def can_create_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we can use any shape which
    # has a finite bounding box
    self.s.is_path()

  def parameters_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we set r and l from the shape's
    # bounding box width and layer
    #self.shape = self.shape.bbox.width() * self.layout.dbu() / 2
    self.l = self.layout.get_info(self.layer)

  def transformation_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we use the center of the shape's
    # bounding box to determine the transformation
    return pya.Trans(self.s.bbox().center())

  def produce_impl(self):

    # This is the main part of the implementation: create the layout

    # fetch the parameters
    ru_dbu = self.ru / self.layout.dbu

    # compute the circle
    pts = []
    #da = math.pi * 2 / self.n
    #for i in range(0, self.n):
      #pts.append(pya.Point.from_dpoint(pya.DPoint(ru_dbu * math.cos(i * da), ru_dbu * math.sin(i * da))))

    # create the shape
    self.cell.shapes(self.l_layer).insert(pya.Polygon(pts))


class PyLib(pya.Library):
  """
  The library where we will put the PCell into
  """

  def __init__(self):

    # Set the description
    self.description = "Python PCell library"

    # Create the PCell declarations
    self.layout().register_pcell("Circle", Circle())
    # That would be the place to put in more PCells ...

    # Register us with the name "MyLib".
    # If a library with that name already existed, it will be replaced then.
    self.register("PyLib")


# Instantiate and register the library
PyLib()
