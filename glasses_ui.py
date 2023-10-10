import sys
import maya.cmds as mc
from PySide2.QtCore import (
    QSize, 
    Qt
)
    
from PySide2.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget,
    QDockWidget,
    QHBoxLayout,
    QVBoxLayout, 
    QPushButton,
    QListWidget
)

from PySide2.QtGui import QPalette, QColor

class GlassesTools(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()

        # Naming and Sizing
        self.setWindowTitle("Glasses Tools")
        self.setFixedSize(QSize(800,600))
        self.setMinimumSize(QSize(600,400))
        self.setMaximumSize(QSize(800,600))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Initial setup
        self.master_widget = QWidget()
        self.master_layout = QHBoxLayout(self.master_widget)
        
        # Layout one
        self.layout_one = QVBoxLayout()
        self.master_layout.addLayout(self.layout_one)
        
        self.button_one = QPushButton("Retransform Asset")
        self.button_one.clicked.connect(self.button_one_clicked)
        self.button_two = QPushButton("Realign Asset")
        self.button_two.clicked.connect(self.button_two_clicked)
        self.button_three = QPushButton("Rotate 90")
        self.button_three.clicked.connect(self.button_three_clicked)
        
        self.list_one = QListWidget()
        self.list_one.SelectionMode(1)
        
        self.layout_one.addWidget(self.button_one)
        self.layout_one.addWidget(self.list_one)
        self.layout_one.addSpacing(100)
        self.layout_one.addWidget(self.button_two)
        self.layout_one.addWidget(self.button_three)
        
        # Layout two
        self.layout_two = QVBoxLayout()
        self.master_layout.addLayout(self.layout_two)

        self.button_four = QPushButton("Button Four")
        self.button_five = QPushButton("Button Five")

        self.list_two = QListWidget()
        self.list_two.SelectionMode(1)
        # names = ['rileigh', 'jeremy', 'conner']

        self.layout_two.addWidget(self.list_two)
        self.layout_two.addWidget(self.button_four)
        self.layout_two.addWidget(self.button_five)

        # Parenting widgets
        self.master_layout.setStretchFactor(self.layout_one, 1)
        self.master_layout.setStretchFactor(self.layout_two, 5)        
        self.setCentralWidget(self.master_widget)
        self.setLayout(self.master_layout)

    # Funcs
    def append_items_to_list(self, list_widget, items):
        for item in items:
            list_widget.addItem(item)
    
    def check_selection_length(self, selection_length, value, range=[], check_range=False):
        check_passed = True

        if selection_length == 0:
            check_passed = False
            mc.warning("Please select an object.")
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

    def check_selection_components(self, type, components):
        check_passed = True

        sel_type = components[0].split('.')[1]
        if len(components) > 1:
            for component in components:
                if type == 'vtx':
                    if sel_type[0] != 'v':
                        check_passed = False
                        mc.warning("Please select a vertex.")
                        return check_passed
        
                if type == 'edge':
                    if sel_type[0] != 'e':
                        check_passed = False
                        mc.warning("Please select an edge.")            
                        return check_passed
                        
                if type == 'face':
                    if sel_type[0] != 'f':
                        check_passed = False
                        mc.warning("Please select a face.")
                        return check_passed                
        else:           
            if type == 'vtx':
                if sel_type[0] != 'v':
                    check_passed = False
                    mc.warning("Please select a vertex.")
                    return check_passed
    
            if type == 'edge':
                if sel_type[0] != 'e':
                    check_passed = False
                    mc.warning("Please select an edge.")            
                    return check_passed
                    
            if type == 'face':
                if sel_type[0] != 'f':
                    check_passed = False
                    mc.warning("Please select a face.")
                    return check_passed

        return check_passed
    
    # added multiselected functionality
    def get_selection_components(self, selection, from_component_type, to_component_type):
        
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
    
    def reset_frozen_asset(self):

        # Setting up mode and axis
        mel.eval('setToolTo $gMove')
        mc.manipMoveContext('Move', e=True, mode=10)
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

    def convert_selection_to_vtx(self, selection):
        
        if '.e[' not in selection: # this is redundant I think
            mc.warning("Please select an edge!")
            return
        vtx_from_selection = mc.polyListComponentConversion(selection, tv=True)
        mc.select(cl=True)
        mc.select(vtx_from_selection)
        
        selected_vtx = mc.ls(sl=True, flatten=True)
        vtx_one_pos = round_vtx_pos(mc.xform(selected_vtx[0], t=True, ws=True, q=True))
        vtx_two_pos = round_vtx_pos(mc.xform(selected_vtx[1], t=True, ws=True, q=True))
        
        vtx_pos_list = [vtx_one_pos, vtx_two_pos]
        selection_mesh = selection.split('.')[0]
        out_data = [selection_mesh, vtx_pos_list]
        
        return out_data
   
    def get_vector_direction(self, vtx_pos):

        pos_one = vtx_pos[0]
        pos_two = vtx_pos[1]
        x_zero, y_zero, z_zero = (pos_one[0] - pos_two[0]) ** 2, (pos_one[1] - pos_two[1]) ** 2, (pos_one[2] - pos_two[2]) ** 2
        
        vector_magnitude = math.sqrt(x_zero + z_zero)
        vector_direction = math.degrees(math.asin((math.sqrt(z_zero)/vector_magnitude)))
        rounded_direction = round(vector_direction, 3)
    
        return rounded_direction
        
    def button_one_clicked(self):
        
        # Prechecks
        length_passed = self.check_selection_length(len(mc.ls(sl=True)), 1)
        if not length_passed:
            return
        component_passed = self.check_selection_components('face', mc.ls(sl=True))
        if not component_passed:
            return
        
        # Retransform object
        face_sel = self.reset_frozen_asset()
      
        # Put edges of selected face in our list
        self.list_one.clear()
        components = self.get_selection_components(face_sel, 'face', 'edge')
        self.append_items_to_list(self.list_one, components)
        
    def button_two_clicked(self):

        selected_item = self.list_one.selectedItems()[0].text()
        obj_of_item = selected_item.split('.')[0]
        vtx_positions = self.convert_selection_to_vtx(selected_item)
        vector_direction = self.get_vector_direction(vtx_positions[1])
        print(vector_direction)
        if vector_direction > 45:
            mc.xform(obj_of_item, ro=[0,-vector_direction,0])
        if vector_direction < 45:
            mc.xform(obj_of_item, ro=[0,vector_direction,0])
        
        mc.makeIdentity(obj_sel, apply=True, t=1, r=1, s=1, n=0)
        return
        
    def button_three_clicked(self):
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
            

window = GlassesTools()
window.show()

# app = QApplication(sys.argv)
# window = GlassesTools()
# window.show()
# app.exec_()