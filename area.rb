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
# DESCRIPTION: Compute area of selected shapes 
#
# Run the script with
#   klayout -rm calc_area.rbm ...
# or put the script as "calc_area.rbm" into the installation path (on Unix for version <=0.21:
# set $KLAYOUTPATH to the installation folder).
#

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

$compute_total_area = MenuAction.new( "Compute total area of selected shapes", "" ) do 

  app = RBA::Application.instance
  mw = app.main_window

  lv = mw.current_view
  if lv == nil
    raise "No view selected"
  end

  total_area = 0.0

  lv.each_object_selected do |obj|

    shape = obj.shape
    layout = lv.cellview(obj.cv_index).layout

    if shape.is_polygon? || shape.is_box? || shape.is_path?
      polygon = shape.polygon
      a = polygon.area
      m = obj.trans.mag * layout.dbu
      total_area += a * m * m
    end

  end

  RBA::MessageBox.info("Total area", "Total area of selected objects is #{total_area} square micron", RBA::MessageBox.b_ok)

end

app = RBA::Application.instance
mw = app.main_window

menu = mw.menu
menu.insert_separator("tools_menu.end", "sep_calc_area")
menu.insert_item("tools_menu.end", "compute_total_area", $compute_total_area)
