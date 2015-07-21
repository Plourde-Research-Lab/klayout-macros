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
# DESCRIPTION: Compute length of selected shapes 
#
# Run the script with
#   klayout -rm calc_length.rbm ...
# or put the script as "calc_length.rbm" into the installation path (on Unix for version <=0.21:
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

$calc_freq = MenuAction.new( "Compute frequency of selected CPW", "Ctl + L" ) do 

  app = RBA::Application.instance
  mw = app.main_window

  lv = mw.current_view
  if lv == nil
    raise "No view selected"
  end

  total_length = 0.0
  
  #CPW consists of  6um wide polygons
  cpw_width = 6.0

  lv.each_object_selected do |obj|

    shape = obj.shape
    layout = lv.cellview(obj.cv_index).layout

    if shape.is_polygon? || shape.is_box? || shape.is_path?
      polygon = shape.polygon
      a = polygon.area
      m = obj.trans.mag * layout.dbu
      total_length += a * m * m / cpw_width
    end

    path = "C:/Users/Caleb/KLayout/macros/calc_freq.py"
    freq = `python #{path} #{total_length}`
    puts freq
    
    text = "Total length of selected resonators is #{total_length}  micron\n"
    text += "Total frequency of selected resonator lengths is #{freq}\n"
  
    RBA::MessageBox.info("Frequency",text , RBA::MessageBox.b_ok)

  end


end

app = RBA::Application.instance
mw = app.main_window

menu = mw.menu
menu.insert_separator("tools_menu.end", "sep_calc_length")
menu.insert_item("tools_menu.end", "calc_freq", $calc_freq)
