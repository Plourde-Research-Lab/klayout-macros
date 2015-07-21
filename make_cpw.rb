class MenuAction < RBA::Action
  def initialize( title, shortcut, &action ) 
    self.title = title
    self.shortcut = shortcut
    @action = action
  end
  def triggered 
    @action.call( self ) 
  end
private
  @action
end

$make_cpw = MenuAction.new( "Make CPW", "" ) do 
  app = Application.instance
  mw = app.main_window
  lv = mw.current_view
  raise "No view selected" if lv.nil?
  ly = lv.active_cellview.layout
  dbu = ly.dbu
  
  ri,ro,n = 95/dbu,105/dbu,10/dbu # Divide by dbu to convert from um to database units (which are integers)
  
<<<<<<< HEAD
  cpw_layer = ly.layer(1,0)
  keepout_layer= ly.layer(1,6)
  
  lv.transaction("Convert Paths to CPW")
=======
  lv.transaction("Convert to polygon then round")
>>>>>>> d9efbde6caeca88b55dc3ceea6fe4add3f996fdc
  
  begin
  
    lv.each_object_selected { |obj|
  
      if !obj.is_cell_inst?
      # Define new paths
       inner = Path.new()
       outer = Path.new()
<<<<<<< HEAD
       keepout = Path.new()
       inner.assign(obj.shape.path)
       outer.assign(obj.shape.path)
       keepout.assign(obj.shape.path)

      # Make outer path wider
       outer.width = 22.0/dbu
       
       #Make keepout wider
       keepout.width = 30.0/dbu
=======
       inner.assign(obj.shape.path)
       outer.assign(obj.shape.path)

      # Make outer path wider
       outer.width = 22.0/dbu
>>>>>>> d9efbde6caeca88b55dc3ceea6fe4add3f996fdc
      
      #Convert to polygon and round corners
       inner = [inner.polygon.round_corners(ri,ro,n)]
       outer = [outer.polygon.round_corners(ri-(6/dbu), ro+(6/dbu), n)]
<<<<<<< HEAD
       keepout = keepout.polygon.round_corners(ri-(10/dbu), ro+(10/dbu), n)
      
       ep = RBA::EdgeProcessor::new
       outer_minus_inner = ep.boolean_p2p(outer, inner, RBA::EdgeProcessor::ModeANotB, true, false)

      #Insert cpw into correct layer
      outer_minus_inner.each do |p|
       lv.active_cellview.cell.shapes(cpw_layer).insert(p)
       end

      #Insert keepout into correct layer
      lv.active_cellview.cell.shapes(keepout_layer).insert(keepout)
=======
      
       ep = RBA::EdgeProcessor::new
       outer_minus_inner = ep.boolean_p2p(outer, inner, RBA::EdgeProcessor::ModeANotB, true, false)
       puts outer_minus_inner.to_s
      #Insert into view in different layers
      outer_minus_inner.each do |p|
       lv.active_cellview.cell.shapes(ly.layer(5,3)).insert(p)
       end
      # lv.active_cellview.cell.shapes(ly.layer(5,4)).insert(outer)
>>>>>>> d9efbde6caeca88b55dc3ceea6fe4add3f996fdc
       
      end  
    }
  
  ensure
    lv.commit
  end
end

app = RBA::Application.instance
mw = app.main_window

menu = mw.menu
menu.insert_item("tools_menu.end", "make_cpw", $make_cpw)