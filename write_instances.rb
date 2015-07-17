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


def print_image_definitions(file, cv, mask_name)

  dbu = cv.layout.dbu
  
  # Scale for Mask, e.g. 4x
  scale = 4
  
  itrans = RBA::ICplxTrans.from_trans(RBA::CplxTrans.new)

  # For each instance placed in cell, write definition
  cv.cell.each_inst do |inst|
    box = inst.bbox.transformed_cplx(itrans)
    width = (box.width*dbu*scale/1000)
    height = (box.height*dbu*scale/1000)
    x = box.center.x*dbu*scale/1000
    y = box.center.y*dbu*scale/1000

    
    job_file_text = "START_SECTION IMAGE_DEFINITION\n"
    job_file_text += "\tIMAGE_ID                                      \"#{inst.cell.basic_name}\"\n"
    job_file_text += "\tRETICLE_ID                                    \"#{mask_name}\"\n"
    job_file_text += "\tIMAGE_SIZE                                    #{"%06f"  % width} #{"%06f"  %  height}\n"
    job_file_text += "\tIMAGE_SHIFT                                  #{"%06f"  % x} #{"%06f"  % y}\n"
    job_file_text += "\tMASK_SIZE                                      #{"%06f"  % width} #{"%06f"  %  height}\n"
    job_file_text += "\tMASK_SHIFT                                    #{"%06f"  % x} #{"%06f"  % y}\n"
    job_file_text += "\tVARIANT_ID                                    \"\"\n"
    job_file_text += "END_SECTION\n\n"
    puts job_file_text
    file.puts(job_file_text)
  end
  
end

$write_instances = MenuAction.new("Write Instances to File", "") do 

  app = RBA::Application.instance
  mw = app.main_window

  # get the current layout view
  lv = mw.current_view
  if lv == nil
    raise "No view selected"
  end

  # get the current cell view (Make sure you're running this on your mask)
  cv = lv.cellview(lv.active_cellview_index)
  if (cv.cell.name.downcase != "mask")
    raise "Make your \"Mask\" cell your current view."
  end
  if !cv.is_valid?
    raise "No layout selected"
  end

  
  # get parameters for job file
  mask_name = RBA::InputDialog.get_string("Mask Name", "Specify the reticle ID", "mask")
  filename = RBA::FileDialog.ask_save_file_name("ASML Job file", "test.asml", "ASML files (*.asml *.txt)")
  
  if filename
    File.open(filename, "w") do |file|
      print_image_definitions(file, cv, mask_name)
    end
  end

end

app = RBA::Application.instance
mw = app.main_window

menu = mw.menu
menu.insert_separator("@hcp_context_menu.end", "write_instances_sep")
menu.insert_item("@hcp_context_menu.end", "write_instances", $write_instances)
