# CPW P-Cell

class CPW(pya.PCellDeclarationHelper):
  """
  The PCell declaration for the cpw
  """

  def __init__(self):

    # Important: initialize the super class
    super(CPW, self).__init__()
    
    #default_path = [pya.DPoint(0,0), pya.DPoint(100,0)]

    # declare the parameters
    self.param("l", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("w", self.TypeDouble, "Width", default = 10.)
    self.param("s", self.TypeShape, "", default = pya.DPoint(0, 0))
    self.param("g", self.TypeDouble, "Gap", default=6.)
    self.param("r", self.TypeDouble, "Radius", default = 100.)
    self.param("n", self.TypeInt, "Number of points", default = 64)     
    self.param("path", self.TypeShape, "", default=pya.Path())
    self.param("name", self.TypeString, "Name", default= "CPW")
    # this hidden parameter is used to determine whether the radius has changed
    # or the "s" handle has been moved
    self.param("ru", self.TypeDouble, "Radius", default = 0.0, hidden = True)
    self.param("rd", self.TypeDouble, "Double radius", readonly = True)


  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return str(self.n)
  
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
    self.shape.is_path()
  
  def parameters_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we set r and l from the shape's 
    # bounding box width and layer
    self.w = self.shape.path.width() * self.layout.dbu()
    self.p = self.shape().path()
  
  def transformation_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we use the center of the shape's
    # bounding box to determine the transformation
    return pya.Trans(sef.shape.bbox().center())
  
  def produce_impl(self):
  
    # This is the main part of the implementation: create the layout

    # fetch the parameters
    dbu = self.layout.dbu
    ru_dbu = self.ru / dbu
    center_width = self.w
    s_width = self.g
    keepout_width=4./dbu
    center_radius = self.r
    ri = center_radius - .5*self.w #Inner radius
    ro = center_radius + .5*self.w # Outer radius
    n = 10/dbu #Number of points per curve
    
    cpw_layer = self.l
    keepout_layer = self.layout.layer(1,6)
    
    # compute the cpw
    inner = pya.Path()
    outer = pya.Path()
    keepout = pya.Path()
    
    inner = self.path
    outer = self.path
    keepout = self.path
    
    #Adjust widths
    inner_width = center_width
    outer_width = inner_width + 2*s_width
    keepout_width = outer_width + 2*keepout_width
    
    #Round Corners
    inner = [inner.polygon().round_corners(ri, ro, n)]
    outer = [outer.polygon().round_corners(ri-s_width,ro+s_width, n)]
    keepout = keepout.polygon().round_corners(ri-s_width-keepout_width, ro+s_width+keepout_width, n)
    
    #Subtract inner from outer
    ep = pya.EdgeProcessor()
    outer_minus_inner = ep.boolean_p2p(outer, inner, pya.EdgeProcessor().ModeANotB, True, False)
    
    for p in outer_minus_inner:
        self.cell.shapes(cpw_layer).insert(p)
    
   # lv.active_cellview().cell.shapes(cpw_layer).insert(outer_minus_inner[0])
    self.cell.shapes(keepout_layer).insert(keepout)
    
    # create the shape
   # self.cell.shapes(self.l_layer).insert(pya.Polygon(pts))
   
class PyLib(pya.Library):

  def __init__(self):
  
    # Set the description
    self.description = "Python PCell library"
    
    # Create the PCell declarations
    self.layout().register_pcell("CPW", CPW())
    # That would be the place to put in more PCells ...
    
    # Register us with the name "MyLib".
    # If a library with that name already existed, it will be replaced then.
    self.register("PyLib")


# Instantiate and register the library
PyLib()
