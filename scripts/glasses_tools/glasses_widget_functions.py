import maya.cmds as mc
import math
from glasses_tools import glasses_utils as glutils

def retransform_asset(current_selection, list_widget):
    
    # Prechecks
    length_passed = glutils.check_selection_length(len(current_selection), 1)
    if not length_passed:
        return
    component_passed = glutils.check_selection_components(current_selection, 'face', absolute=True)

    if not component_passed or component_passed == 'non_component':
        mc.warning("Please select a face.")
        return

    # Retransform object
    face_sel = glutils.reset_frozen_asset()

    # Put edges of selected face in our list
    list_widget.clear()
    components = glutils.get_selection_components(face_sel, 'face', 'edge')
    glutils.append_items_to_list(list_widget, components)

def realign_asset(self):

    # Prechecks
    component_passed = self.check_selection_components(self.list_one.selectedItems()[0].text(), 'edge', absolute=True)
    if not component_passed or component_passed == 'non_component':
        mc.warning("Please select an edge")
        return
    
    selected_item = self.list_one.selectedItems()[0].text()
    obj_of_item = selected_item.split('.')[0]

    vtx_positions = self.convert_selection_to_components(selected_item, 'vtx')
    vector_direction = self.get_vector_direction(vtx_positions[2])

    if vector_direction == 'same':
        mc.warning(f"{selected_item} is already aligned.")
        return

    if (math.isclose(vtx_positions[2][0][0], vtx_positions[2][1][0], abs_tol = 0.0011) or 
        math.isclose(vtx_positions[2][0][2], vtx_positions[2][1][2], abs_tol = 0.0011)):
        mc.warning(f"{selected_item} is already aligned.")
        return

    while True:
        obj_rot = mc.xform(obj_of_item, ro=True, q=True)[1]
        mc.xform(obj_of_item, ro=[0,obj_rot-vector_direction,0])

        vtx_one_pos = mc.xform(vtx_positions[1][0], t=True, ws=True, q=True)
        for pos in vtx_one_pos:
            vtx_one_pos[vtx_one_pos.index(pos)] = round(pos, 3)

        vtx_two_pos = mc.xform(vtx_positions[1][1], t=True, ws=True, q=True)
        for pos in vtx_two_pos:
            vtx_two_pos[vtx_two_pos.index(pos)] = round(pos, 3)
        
        if vtx_one_pos[0] == vtx_two_pos[0] or vtx_one_pos[2] == vtx_two_pos[2]:
            break

        elif (math.isclose(vtx_one_pos[0], vtx_two_pos[0], abs_tol = 0.0011) or 
                math.isclose(vtx_one_pos[2], vtx_two_pos[2], abs_tol = 0.0011)):
            break

    mc.makeIdentity(obj_of_item, apply=True, t=1, r=1, s=1, n=0)
    return
    
def rotate_ninety():
    cur_sel = mc.ls(sl=True)[0]
    if '.' in cur_sel:
        mc.select(cl=True)
        mc.select(cur_sel.split('.'))[0]
        cur_sel = mc.ls(sl=True)[0]
        
    cur_rot = mc.xform(cur_sel, ro=True, q=True)[1]            
    mc.move(0,0,0, f'{cur_sel}.scalePivot', f'{cur_sel}.rotatePivot', a=True)
    mc.manipPivot(o=[0,0,0])
    mc.xform(cur_sel, ro=[0,cur_rot + 90,0])
    
    mc.makeIdentity(cur_sel, apply=True, t=1, r=1, s=1, n=0)
    return

def center_selection_button_clicked():
    cur_sel = mc.ls(sl=True)
    sel_type = glutils.check_selection_components(components=cur_sel)

    if not glutils.check_selection_length(len(cur_sel), 1):
        return

    if sel_type == 'non_component':
        mc.warning("Please select a vtx, edge, or face.")
        return

    cur_obj = cur_sel[0].split('.')[0]
    obj_pos = mc.xform(cur_obj, t=True, q=True)
    
    if sel_type == 'vtx':
        mc.makeIdentity(cur_obj, apply=True, t=1, r=1, s=1, n=0)
        cur_pos = mc.xform(cur_sel[0], t=True, q=True)
        mc.xform(cur_obj, t=[-cur_pos[0], obj_pos[1], -cur_pos[2]])

    if sel_type == 'edge':
        pass
    
    if sel_type == 'face':
        pass
    
    mc.makeIdentity(cur_obj, apply=True, t=1, r=1, s=1, n=0)
    return