  app = Application.instance
  mw = app.main_window
  lv = mw.current_view
  raise "No view selected" if lv.nil?
  ly = lv.active_cellview.layout
  dbu = ly.dbu
  
 lv.transaction("Duplicate")
  
  begin
  
    lv.each_object_selected { |obj|
  
      if !obj.is_cell_inst?
       s = Shapes.new()
       shape = s.insert(obj.shape)
      # layer_index = ly.insert_layer(RBA::LayerInfo::new(1,5))
       #puts layer_index
        
      if shape.is_path?
          shape.polygon = shape.path.polygon # polygon= method replaces the shape with that polygon while preserving user properties. 
      end
  
      # Now that we have a polygon we round the corners
       shape.polygon =  shape.polygon.round_corners(95/dbu,105/dbu,100)
       #shape.polygon = new_polygon
       puts shape.polygon
       lv.active_cellview.cell.shapes(ly.layer(1,3)).insert(shape.polygon)
     end  
     }
  
  ensure
    lv.commit
  end