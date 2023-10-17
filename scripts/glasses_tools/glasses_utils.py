import maya.cmds as mc
import maya.mel as mc
import math

def make_variables_for_instancing(name, num_instances):
    variable_list = []
    ones = {1:'one', 2:'two', 3:'three', 
            4:'four', 5:'five', 6:'six', 
            7:'seven', 8:'eight', 9:'nine'}

    special = { 10:'ten', 11:'eleven', 12:'twelve',
                13:'thirteen', 14:'fourteen', 15:'fifteen',
                16:'sixteen', 17:'seventeen', 18:'eighteen',
                19:'nineteen'}

    tens = {2:'twenty', 3:'thirty', 4:'forty', 
            5:'fifty', 6:'sixty', 7:'seventy', 
            8:'eighty', 9:'ninety'}
        
    def int_to_word(integer):
        int_place = ''
        if num_instances == 0:
            print("Cannot make zero instances. Zero instances made.")
            return int_place
        
        elif num_instances > 99:
            print("Cannot make more than 99 instances. Zero instances made")
            return int_place

        elif num_instances < 10:
            int_place = 'ones'

        elif num_instances >= 10 and num_instances <= 100:
            int_place = 'tens'

        return int_place
    
    int_place = int_to_word(num_instances)
    if not int_place:
        return

    for num in range(1, num_instances+1):
        if int_place == 'ones':
            cur_instance = f"{name}_{ones[num]}"
    
        if int_place == 'tens':
            if num < 10:
                cur_instance = f"{name}_{ones[num]}"
            
            elif 10 <= num <= 19:
                cur_instance = f"{name}_{special[num]}"

            elif num >= 20:
                if (num == 20 or
                    num == 30 or
                    num == 40 or
                    num == 50 or
                    num == 60 or
                    num == 70 or
                    num == 80 or
                    num == 90
                    ):
                    cur_instance = f"{name}_{tens[int(str(num)[0])]}"
                
                else:
                    cur_instance = f"{name}_{tens[int(str(num)[0])]}_{ones[int(str(num)[1])]}"

        if cur_instance not in variable_list:
            variable_list.append(cur_instance)

            
    print(variable_list)
    return variable_list

def append_items_to_list(list_widget, items):
    for item in items:
        list_widget.addItem(item)

def check_selection_length(selection_length, value, range=[], check_range=False):
    check_passed = True
    
    # add type to mc.warning
    if selection_length == 0:
        check_passed = False
        mc.warning("Cannot have empty selection. Please select something.")
        return check_passed

    if check_range:
        if range[0] < 1 or range[1] < 1:
            mc.warning("Please make sure the range values are greater than one.")
            return
            
        if not range[0] < range[1]:
            mc.warning("Please make sure the input ranges are as such: [lesser, greater].")
            return
        
        if not range[1] < selection_length < range[0]:
            check_passed = False
            mc.warning(f"Please select a number of objects between {range[0]} and {range[1]}")
            return check_passed
    
    if value < 1:
        mc.warning("Please set a value greater than 0.")
        return

    if selection_length != value:
        if value == 1:
            check_passed = False
            mc.warning("Please select 1 object.")
            return check_passed
            
        if value > 1:
            check_passed = False
            mc.warning(f"Please select {value} objects.")
            return check_passed

    return check_passed

def check_selection_components(components, type='', absolute=False):
    check_passed = True
    component_type = ''

    try:
        if isinstance(components, list):
            sel_type = components[0].split('.')[1][0]
        else:
            sel_type = components.split('.')[1][0]
        
    except:
        component_type = 'non_component'
        return component_type

    if absolute:         
        if type == 'vtx':
            if sel_type != 'v':
                check_passed = False
                mc.warning("Please select a vertex.")
                return check_passed

        if type == 'edge':
            if sel_type != 'e':
                check_passed = False
                mc.warning("Please select an edge.")            
                return check_passed
                
        if type == 'face':
            if sel_type != 'f':
                check_passed = False
                mc.warning("Please select a face.")
                return check_passed
                
        return check_passed
                
    else:
        if sel_type == 'v':
            component_type = 'vtx'
            return component_type

        if sel_type == 'e':
            component_type = 'edge'
            return component_type

        if sel_type == 'f':
            component_type = 'face'
            return component_type 

# added multiselected functionality
def get_selection_components(selection, from_component_type, to_component_type):
    
    if to_component_type == 'vtx':
        selection = mc.polyListComponentConversion(selection, tv=True)
        components = mc.ls(selection, flatten=True)
        return components

    if to_component_type == 'edge':
        selection = mc.polyListComponentConversion(selection, te=True)
        components = mc.ls(selection, flatten=True)
        return components

    if to_component_type == 'face':
        selection = mc.polyListComponentConversion(selection, tf=True)
        components = mc.ls(selection, flatten=True)
        return components

def reset_frozen_asset():

    # Setting up mode and axis
    mel.eval('setToolTo $gMove')
    mc.manipMoveContext('Move', e=True, mode=10)
    mel.eval("string $objs[] = `ls -sl -type transform -type geometryShape`;if (size($objs) > 0) { xform -cp; } manipPivot -rp -ro;")
    manip_pos = mc.manipMoveContext('Move', p=True, q=True)
    
    # Get selection information
    face_sel = mc.ls(sl=True)[0]
    obj_sel = face_sel.split('.')[0]
    ref_grp = mc.group(w=True, em=True)
    grp_sel = mc.ls(sl=True)[0]
    mc.select(cl=True)
    
    # Move reference group and grab data
    mc.move(manip_pos[0], manip_pos[1], manip_pos[2], ref_grp)
    constrain = mc.normalConstraint(obj_sel, ref_grp, aim=[0,0,1], wut=0)
    mc.delete(constrain)
    ref_translate = mc.xform(grp_sel, t=True, q=True)
    ref_rotate = mc.xform(grp_sel, ro=True, q=True)
    
    # Get obj current transform and add reference transforms
    cur_translate = mc.xform(obj_sel, t=True, q=True)
    cur_rotate = mc.xform(obj_sel, ro=True, q=True)
    mc.parent(obj_sel, ref_grp)
    mc.xform(ref_grp, t=[0,0,0])
    mc.xform(ref_grp, ro=[0,0,0])
    mc.parent(obj_sel, w=True)
    mc.delete(ref_grp)
    mc.makeIdentity(obj_sel, apply=True, t=1, r=1, s=1, n=0)
    mc.move(0,0,0, f'{obj_sel}.scalePivot', f'{obj_sel}.rotatePivot', a=True)
    mc.xform(obj_sel, ro=[90,0,0])
    mc.makeIdentity(obj_sel, apply=True, t=1, r=1, s=1, n=0)
    
    return face_sel

def round_vtx_pos(pos_list):

    new_pos_list = []
    for pos in pos_list:
        new_pos = round(pos, 3)
        
        new_pos_list.append(new_pos)
    return new_pos_list

def convert_selection_to_components(selection, type):
    
    if type == 'vtx':
        component_from_selection = mc.polyListComponentConversion(selection, tv=True)
    if type == 'edge':
        component_from_selection = mc.polyListComponentConversion(selection, te=True)
    if type == 'face':
        component_from_selection = mc.polyListComponentConversion(selection, tf=True)

    mc.select(cl=True)
    mc.select(component_from_selection)
    
    selected_components = mc.ls(sl=True, flatten=True)
    pos_one = round_vtx_pos(mc.xform(selected_components[0], t=True, ws=True, q=True))
    pos_two = round_vtx_pos(mc.xform(selected_components[1], t=True, ws=True, q=True))
    
    pos_list = [pos_one, pos_two]
    selection_mesh = selection.split('.')[0]
    out_data = [selection_mesh, selected_components, pos_list]
    
    return out_data

def get_vector_direction(vtx_pos):

    if vtx_pos[0][0] <= vtx_pos[1][0]:
        pos_one = vtx_pos[0]
        pos_two = vtx_pos[1]
    
    elif vtx_pos[0][0] >= vtx_pos[1][0]:
        pos_one = vtx_pos[1]
        pos_two = vtx_pos[0]
    x_zero, y_zero, z_zero = (pos_one[0] - pos_two[0]) ** 2, (pos_one[1] - pos_two[1]) ** 2, (pos_one[2] - pos_two[2]) ** 2
    
    vector_magnitude = math.sqrt(x_zero + z_zero)
    vector_direction = math.degrees(math.asin((math.sqrt(z_zero)/vector_magnitude)))
    rounded_direction = round(vector_direction, 3)
    
    if str(rounded_direction).split('.')[0] == '001':
        rounded_direction = round(rounded_direction, 2)
    
    elif str(rounded_direction).split('.')[1] == '999':
        rounded_direction = round(rounded_direction, 2)
    
    elif rounded_direction > 45:
        rounded_direction = 90-rounded_direction
    
    elif pos_one[2] < pos_two[2]:
        rounded_direction = -rounded_direction
    
    elif pos_one[0] == pos_two[0] or pos_one[2] == pos_two[2]:
        rounded_direction = 'same'
        
    return rounded_direction

def printer():
    print("HELLO WORLD")