import sys
import maya.cmds as mc
import maya.mel as mel
import math
from PySide2.QtCore import (
    QSize, 
    Qt,
    QTimer
)
    
from PySide2.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget,
    QDockWidget,
    QHBoxLayout,
    QVBoxLayout, 
    QPushButton,
    QListWidget,
    QDial
)

from PySide2.QtGui import QPalette, QColor

class GlassesTools(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()

        # Naming and Sizing
        self.window_name = "Glasses Tools"
        self.setWindowTitle(self.window_name)
        self.setFixedSize(QSize(800,600))
        self.setMinimumSize(QSize(600,400))
        self.setMaximumSize(QSize(800,600))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Make sure only one window
        if mc.window(self.window_name, ex = True):
            mc.deleteUI(self.window_name)

        # Initial setup
        self.master_widget = QWidget()
        self.master_layout = QHBoxLayout(self.master_widget)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.is_list_one_selected)
        self.timer.start(10)


        # Layout one
        self.layout_one = QVBoxLayout()
        self.master_layout.addLayout(self.layout_one)
        
        self.retransform_asset_button = QPushButton("Retransform Asset")
        self.center_selection_button = QPushButton("Center Selection")
        self.realign_asset_button = QPushButton("Realign Asset")
        self.realign_asset_button.setEnabled(False)
        self.rotate_ninety_button = QPushButton("Rotate 90")

        self.retransform_asset_button.clicked.connect(self.retransform_asset_button_clicked)
        self.center_selection_button.clicked.connect(self.center_selection_button_clicked)
        self.realign_asset_button.clicked.connect(self.realign_asset_button_clicked)
        self.rotate_ninety_button.clicked.connect(self.rotate_ninety_button_clicked)
        
        self.list_one = QListWidget()
        self.list_one.SelectionMode(1)
        
        self.layout_one.addSpacing(10)
        self.layout_one.addWidget(self.retransform_asset_button)
        self.layout_one.addWidget(self.list_one)
        self.layout_one.addWidget(self.center_selection_button)
        self.layout_one.addWidget(self.realign_asset_button)
        self.layout_one.addWidget(self.rotate_ninety_button)
        self.layout_one.addSpacing(50)

        # Layout two
        self.dial_dummy_one = QWidget()
        self.dial_dummy_two = QWidget()
        self.dial_dummy_three = QWidget()

        self.layout_two = QVBoxLayout()
        self.horizontal_one = QHBoxLayout(self.dial_dummy_one)
        self.horizontal_two = QHBoxLayout(self.dial_dummy_two)
        self.horizontal_three = QHBoxLayout(self.dial_dummy_three)
        self.layout_two.addLayout(self.horizontal_one)
        self.master_layout.addLayout(self.layout_two)


        self.button_four = QPushButton("Button Four")
        self.button_five = QPushButton("Button Five")

        self.list_two = QListWidget()
        self.list_two.SelectionMode(1)
        
        self.dial_one = QDial()
        self.dial_one.setNotchesVisible(True)
        self.dial_one.setRange(1,100)
        self.dial_one.setValue(50)
        self.dial_two = QDial()
        self.dial_two.setNotchesVisible(True)
        self.dial_two.setRange(1,100)
        self.dial_two.setValue(50)
        self.dial_three = QDial()
        self.dial_three.setNotchesVisible(True)
        self.dial_three.setRange(1,100)
        self.dial_three.setValue(50)
        self.dial_four = QDial()
        self.dial_four.setNotchesVisible(True)
        self.dial_four.setRange(1,100)
        self.dial_four.setValue(50)
        self.dial_five = QDial()
        self.dial_five.setNotchesVisible(True)
        self.dial_five.setRange(1,100)
        self.dial_five.setValue(50)
        self.dial_six = QDial()
        self.dial_six.setNotchesVisible(True)
        self.dial_six.setRange(1,100)
        self.dial_six.setValue(50)
        self.dial_seven = QDial()
        self.dial_seven.setNotchesVisible(True)
        self.dial_seven.setRange(1,100)
        self.dial_seven.setValue(50)
        self.dial_eight = QDial()
        self.dial_eight.setNotchesVisible(True)
        self.dial_eight.setRange(1,100)
        self.dial_eight.setValue(50)
        self.dial_nine= QDial()
        self.dial_nine.setNotchesVisible(True)
        self.dial_nine.setRange(1,100)
        self.dial_nine.setValue(50)
        

        self.layout_two.addWidget(self.list_two)
        self.horizontal_one.addWidget(self.dial_one)
        self.horizontal_one.addWidget(self.dial_two)
        self.horizontal_one.addWidget(self.dial_three)
        self.horizontal_two.addWidget(self.dial_four)
        self.horizontal_two.addWidget(self.dial_five)
        self.horizontal_two.addWidget(self.dial_six)
        self.horizontal_three.addWidget(self.dial_seven)
        self.horizontal_three.addWidget(self.dial_eight)
        self.horizontal_three.addWidget(self.dial_nine)
        self.layout_two.addWidget(self.dial_dummy_one)
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

    def check_selection_components(self, components, type='', absolute=False):
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

    def round_vtx_pos(self, pos_list):
    
        new_pos_list = []
        for pos in pos_list:
            new_pos = round(pos, 3)
            
            new_pos_list.append(new_pos)
        return new_pos_list
    
    def convert_selection_to_components(self, selection, type):
        
        if type == 'vtx':
            component_from_selection = mc.polyListComponentConversion(selection, tv=True)
        if type == 'edge':
            component_from_selection = mc.polyListComponentConversion(selection, te=True)
        if type == 'face':
            component_from_selection = mc.polyListComponentConversion(selection, tf=True)

        mc.select(cl=True)
        mc.select(component_from_selection)
        
        selected_components = mc.ls(sl=True, flatten=True)
        pos_one = self.round_vtx_pos(mc.xform(selected_components[0], t=True, ws=True, q=True))
        pos_two = self.round_vtx_pos(mc.xform(selected_components[1], t=True, ws=True, q=True))
        
        pos_list = [pos_one, pos_two]
        selection_mesh = selection.split('.')[0]
        out_data = [selection_mesh, selected_components, pos_list]
        
        return out_data
   
    def get_vector_direction(self, vtx_pos):

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

    def is_list_one_selected(self):
        if self.list_one.selectedItems():
            self.realign_asset_button.setEnabled(True)
        else:
            self.realign_asset_button.setEnabled(False)

    def retransform_asset_button_clicked(self):
        
        # Prechecks
        length_passed = self.check_selection_length(len(mc.ls(sl=True)), 1)
        if not length_passed:
            return
        component_passed = self.check_selection_components(mc.ls(sl=True), 'face', absolute=True)

        if not component_passed or component_passed == 'non_component':
            mc.warning("Please select a face.")
            return
    
        # Retransform object
        face_sel = self.reset_frozen_asset()
    
        # Put edges of selected face in our list
        self.list_one.clear()
        components = self.get_selection_components(face_sel, 'face', 'edge')
        self.append_items_to_list(self.list_one, components)

        # if self.list_one.count() > 0:
        #     self.realign_asset_button.setEnabled(True)
        
        # elif self.list_one.count() == 0:
        #     self.realign_asset_button.setEnabled(False)
            
    def realign_asset_button_clicked(self):

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
        
    def rotate_ninety_button_clicked(self):
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
    
    def center_selection_button_clicked(self):
        cur_sel = mc.ls(sl=True)
        sel_type = self.check_selection_components(components=cur_sel)

        
        if not self.check_selection_length(len(cur_sel), 1):
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
        
        mc.makeIdentity(obj_of_item, apply=True, t=1, r=1, s=1, n=0)
        return

if __name__ == '__main__':
    window = GlassesTools()
    window.show()

    # app = QApplication(sys.argv)
    # window = GlassesTools()
    # window.show()
    # app.exec_()
    
