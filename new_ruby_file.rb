
# Enter your Ruby code here

#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# DESCRIPTION: Write all child cells of the current cell to individual files
#
# Install the script with
#   klayout -rm write_childcells.rbm ...
# or put the script as "write_childcells.rbm" into the installation path 
# (on Unix for version <=0.21: set $KLAYOUTPATH to the installation folder).
#
# The script installs a new menu entry at the end of the cell list context
# menu: "Write Child Cells". This function asks for the hierarchy level and 
# writes all cells at this level (below the current cell) to files called 
# "{cellname}.gds".

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

# Collect all cells at hiearchy level "level" below the cell "from_cell"


# into the array "cells" which is used as a set. 
# The keys of "cells" will be the cell indexes of the cells collected.
def get_cells_at_hierarchy_level(layout, from_cell, level, cells)
  from_cell.each_child_cell do |cc| 
    if level == 1
      cells[cc] = 1
    else
      get_cells_at_hierarchy_level(layout, layout.cell(cc), level - 1, cells)
    end
  end
end

def get_instances(cell, instances)
  cell.each_inst do |inst|
    instances.push(inst)
  end
end

$write_child_cells = MenuAction.new("Write Mask Info to Job File", "") do 

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

  # fetch the hierarchy level from which to write the cells
  level = RBA::InputDialog.get_int_ex("Hierachy Level", "Specify the hierarchy level below cell #{cv.layout.cell_name(cv.cell_index)}, layout @#{lv.active_cellview_index+1} from which to write the cells", 1, 1, 1000, 1)
  if level.has_value?


  dbu = cv.layout.dbu
    # gather the cells to write
  cells_to_write = {}
   get_cells_at_hierarchy_level(cv.layout, cv.cell, level.value, cells_to_write)
    #get_instances(cv.cell, instances)
    
    itrans = RBA::ICplxTrans.from_trans(RBA::CplxTrans.new)
    cv.cell.each_inst do |inst|
      box = inst.bbox.transformed_cplx(itrans)
      puts "X: #{box.center.to_s}"
      puts "Y: #{box.center.to_s}"
    end

    # loop over all child cells of the current cell
    cells_to_write.each do |cc,dummy|

      # make a cell object reference from the cell index
      child_cell = cv.layout.cell(cc)
      

      # get the cell' information
      cell_name = cv.layout.cell_name(cc)
      cell_width = child_cell.bbox.right*dbu - child_cell.bbox.left*dbu
      cell_height = child_cell.bbox.top*dbu - child_cell.bbox.bottom*dbu
      cell_x = child_cell.bbox.center.x*dbu
      cell_y = child_cell.bbox.center.y*dbu
      

      text = ""
      text =  "Name: #{cell_name}\n"
      text +=  "Width: #{cell_width}\n"
      text +=  "Height: #{cell_height}\n"
      text += "X: #{cell_x}\n"
      text += "Y: #{cell_y}\n"
      puts text

 job_file_text = " START_SECTION IMAGE_DEFINITION
     IMAGE_ID                                      \"#{cell_name}\"
     RETICLE_ID                                    \"\"
     IMAGE_SIZE                                    1.260000 0.480000
     IMAGE_SHIFT                                   18.000000 36.000000
     MASK_SIZE                                     1.264000 0.480000
     MASK_SHIFT                                    18.000000 36.000000
     VARIANT_ID                                    ""
  END_SECTION\n\n"

    end

  end

end

app = RBA::Application.instance
mw = app.main_window

menu = mw.menu
menu.insert_separator("@hcp_context_menu.end", "write_childcells_sep")
menu.insert_item("@hcp_context_menu.end", "write_childcells", $write_child_cells)


