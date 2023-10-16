import sys
from PySide2.QtCore import (
    QSize, 
    Qt,
    QTimer
)
    
from PySide2.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget,
    QSizePolicy,
    QDockWidget,
    QHBoxLayout,
    QVBoxLayout, 
    QPushButton,
    QListWidget,
    QTabWidget,
    QSlider,
    QDial
)



from PySide2.QtGui import QPalette, QColor, QFont, QFontMetrics

class CustomChanges(QSlider):
    def __init__(self, orientation):
        super().__init__(orientation)

    def snap_slider(self, change):
        if change == QSlider.SliderValueChange:


class GlassesTools(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()

        # Naming and Sizing
        self.window_name = "Glasses Tools"
        self.setWindowTitle(self.window_name)
        self.setFixedSize(QSize(800,600))
        self.setMinimumSize(QSize(800,600))
        self.setMaximumSize(QSize(1200,800))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Make sure only one window
        if mc.window(self.window_name, ex = True):
            mc.deleteUI(self.window_name)

        # Initial setup
        self.master_widget = QWidget()
        self.master_layout = QHBoxLayout(self.master_widget)
        self.master_tab = QTabWidget()
        self.master_layout.addWidget(self.master_tab)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.is_list_one_selected)
        self.timer.start(10)

        # Tab one
        self.tab_one_widget = QWidget()
        self.master_tab_one_layout = QHBoxLayout(self.tab_one_widget)
    
        # Tab one, layout one
        self.tab_one_layout_one = QVBoxLayout(self.tab_one_widget)
        self.master_tab_one_layout.addLayout(self.tab_one_layout_one)
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
        
        self.tab_one_layout_one.addSpacing(10)
        self.tab_one_layout_one.addWidget(self.retransform_asset_button)
        self.tab_one_layout_one.addWidget(self.list_one)
        self.tab_one_layout_one.addWidget(self.center_selection_button)
        self.tab_one_layout_one.addWidget(self.realign_asset_button)
        self.tab_one_layout_one.addWidget(self.rotate_ninety_button)
        self.tab_one_layout_one.addSpacing(50)

        # Tab one, layout two
        self.tab_one_layout_two = QVBoxLayout()
        self.master_tab_one_layout.addLayout(self.tab_one_layout_two)
        self.horizontal_dummy_one = QWidget()
        self.horizontal_dummy_two = QWidget()
        self.horizontal_dummy_three = QWidget()
        self.horizontal_one = QHBoxLayout(self.horizontal_dummy_one)
        self.horizontal_two = QHBoxLayout(self.horizontal_dummy_two)
        self.horizontal_three = QHBoxLayout(self.horizontal_dummy_three)

        self.variable_list = self.make_variables_for_instancing('vertical_dummy', 3)
        for self.var in self.variable_list:
            self.widget = QWidget()
            self.var = QVBoxLayout(self.widget)
            # self.var.setAlignment(Qt.AlignCenter)
            self.horizontal_one.addWidget(self.widget)

            self.dial = QDial()
            self.dial.setNotchTarget(0.0)
            self.dial.setNotchesVisible(True)
            self.dial.setRange(1,20)
            self.dial.setValue(50)

            self.slider = QSlider(Qt.Horizontal)
            self.slider.setMinimum(0)
            self.slider.setMaximum(100)
            self.slider.setValue(20)
            self.slider.setTickPosition(QSlider.TicksBelow)
            self.slider.setTickInterval(100)
            # self.button.setFixedSize(50,50)z
            # self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            # self.font = self.button.font()
            # self.font_metrics = QFontMetrics(self.font)
            # self.font_width = self.font_metrics.width(self.button.text())
            # self.font_height = self.font_metrics.height()
            # self.button.setMinimumSize(self.font_width, self.font_height)
            # self.button.setMaximumSize(self.font_width*2, self.font_height*2)
            # self.button.adjustSize()

            self.var.addWidget(self.dial)
            self.var.addWidget(self.slider)

        self.variable_list = self.make_variables_for_instancing('vertical_dummy', 3)
        for self.var in self.variable_list:
            self.widget = QWidget()
            self.var = QVBoxLayout(self.widget)
            self.horizontal_two.addWidget(self.widget)

            self.dial = QDial()
            self.dial.setNotchesVisible(True)
            self.dial.setRange(1,20)
            self.dial.setValue(50)

            self.button = QPushButton("Test")

            self.var.addWidget(self.dial)
            self.var.addWidget(self.button)

        self.variable_list = self.make_variables_for_instancing('vertical_dummy', 3)
        for self.var in self.variable_list:
            self.widget = QWidget()
            self.var = QVBoxLayout(self.widget)
            self.horizontal_three.addWidget(self.widget)

            self.dial = QDial()
            self.dial.setNotchesVisible(True)
            self.dial.setRange(1,20)
            self.dial.setValue(50)

            self.button = QPushButton("Test")

            self.var.addWidget(self.dial)
            self.var.addWidget(self.button)

        self.button_four = QPushButton("Button Four")
        self.button_five = QPushButton("Button Five")

        # self.list_two = QListWidget()
        # self.list_two.SelectionMode(1)

        self.tab_one_layout_two.addWidget(self.horizontal_dummy_one)
        self.tab_one_layout_two.addWidget(self.horizontal_dummy_two)
        self.tab_one_layout_two.addWidget(self.horizontal_dummy_three)
        # self.tab_one_layout_two.addWidget(self.list_two)
        # self.tab_one_layout_two.addWidget(self.button_four)
        # self.tab_one_layout_two.addWidget(self.button_five)

        # Tab two
        self.tab_two_widget = QWidget()
        self.master_tab_two_layout = QHBoxLayout(self.tab_two_widget)
        

        # Parenting widgets
        self.master_tab.addTab(self.tab_one_widget, "Asset Adjust")
        self.master_tab.addTab(self.tab_two_widget, "Pack and Ship")
        self.master_tab_one_layout.setStretchFactor(self.tab_one_layout_one, 1)
        self.master_tab_one_layout.setStretchFactor(self.tab_one_layout_two, 5)        
        self.setCentralWidget(self.master_widget)
        self.setLayout(self.master_layout)

    # Funcs
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
        sel_type = check_selection_components(components=cur_sel)

        
        if not check_selection_length(len(cur_sel), 1):
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

if __name__ == '__main__':
    try:
        window.close()
        window.deleteLater()
    except:
        pass

    window = GlassesTools()
    window.show()

    # app = QApplication(sys.argv)
    # window = GlassesTools()
    # window.show()
    # app.exec_()
    

