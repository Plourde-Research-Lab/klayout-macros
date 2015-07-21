require "json"

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

$make_gnd_straps = MenuAction.new( "Make Grounding Straps", "" ) do 
  app = Application.instance
  mw = app.main_window
  lv = mw.current_view
  raise "No view selected" if lv.nil?
  ly = lv.active_cellview.layout
  dbu = ly.dbu
  
  ri,ro,n = 95/dbu,105/dbu,10/dbu # Divide by dbu to convert from um to database units (which are integers)
  
  cpw_layer = ly.layer(1,0)
  keepout_layer= ly.layer(1,6)
  
  lv.transaction("Make Grounding Straps")
  
  begin
  
    lv.each_object_selected { |obj|
  
      if !obj.is_cell_inst?
      # Define new paths
          if obj.shape.is_path?
          new_path = Array.new()
            path = obj.shape.path
             path.each_point do |pt|
              new_path.push << pt
             end
             
             string = new_path.map{|pt| {x: pt.x, y: pt.y}}
             puts string.to_json
             
          end
       
      end  
    }
  
  ensure
    lv.commit
  end
end

app = RBA::Application.instance
mw = app.main_window

menu = mw.menu
menu.insert_item("tools_menu.end", "make_gnd_straps", $make_gnd_straps)