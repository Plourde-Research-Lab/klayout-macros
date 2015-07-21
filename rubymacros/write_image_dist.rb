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


def loop_through_die(cv)

  dbu = cv.layout.dbu
  
  itrans = RBA::ICplxTrans.from_trans(RBA::CplxTrans.new)
  
  cv.cell.each_inst do |inst|
  
    box = inst.bbox.transformed_cplx(itrans)
    xind = box.center.x / box.width
    yind = box.center.y / box.height
     
    itrans = RBA::ICplxTrans.from_trans(RBA::CplxTrans.new)

    inst.cell.each_inst do |inst|
    
      box = inst.bbox.transformed_cplx(itrans)
      x = box.center.x*dbu/1000
      y = box.center.y*dbu/1000
      instance = "<Default>"

      text ="START_SECTION IMAGE_DISTRIBUTION\n"
      text += "\tIMAGE_ID                                      \"#{inst.cell.basic_name}\"\n"
      text += "\tINSTANCE_ID                                   \"#{instance}\"\n"
      text += "\tCELL_SELECTION                                \"#{xind}\" \"#{yind}\"\n"
      text += "\tDISTRIBUTION_ACTION                           \"I\"\n"
      text += "\tOPTIMIZE_ROUTE                                \"N\"\n"
      text += "\tIMAGE_CELL_SHIFT                              #{"%06f"  % x} #{"%06f"  % y}\n"
      text += "END_SECTION\n\n"
      
      puts(text)
      
    end
    
  end
  
end
  

$write_distribution = MenuAction.new("Write Distribution to File", "") do 

  app = RBA::Application.instance
  mw = app.main_window

  # get the current layout view
  lv = mw.current_view
  if lv == nil
    raise "No view selected"
  end

  # get the current cell view (the one selected in the hierarchy browser)
  cv = lv.cellview(lv.active_cellview_index)
  if !cv.is_valid?
    raise "No layout selected"
  end

  
  
 # mask_name = RBA::InputDialog.get_string("Mask Name", "Specify the reticle ID", "mask")
  #filename = RBA::FileDialog.ask_save_file_name("ASML Job file", "test.asml", "ASML files (*.asml *.txt)")
  
 # if filename
  #  File.open(filename, "w") do |file|
    
    #print_image_distributions(cv)
    loop_through_die(cv)
    
   # end

end

app = RBA::Application.instance
mw = app.main_window

menu = mw.menu
menu.insert_separator("@hcp_context_menu.end", "write_dist_sep")
menu.insert_item("@hcp_context_menu.end", "write_distribution", $write_distribution)