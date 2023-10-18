import maya.cmds as mc
import maya.mel as mel
import math
import importlib
from scripts.rools import rools_utils as rootils
from scripts.rools import rools_library as roolibs
importlib.reload(rootils)
importlib.reload(roolibs)

def create_shader(name="myShader", node="VRayMtl"):
    mtl = mc.shadingNode(node, name=name, asShader=True)
    sg = mc.sets(name=f"{name}SG", em=True, r=True, nss=True)
    mc.connectAttr(f"{mtl}.outColor", f"{sg}.surfaceShader")
    
def create_light(name="myLight", node="VRayLightDomeShape", env=False):
    
    if node == "VRayLightDomeShape":
        lgt = mc.shadingNode(node, name=name, asLight=True)
        
        if env:
            file = mc.shadingNode("file", asTexture=True, isColorManaged=True)
            place_txt = mc.shadingNode("place2dTexture", asUtility=True)

            print(file, place_txt)
            for input, output in links.items():
                mc.connectAttr(f"{place_txt}.{input}", f"{file}.{output}")

def toggle_cb_attributes(sel_list, tr=True, ro=True, sc=True, vis=False, lock=False):
    for sel in sel_list:
        if tr:
            for attr in roolibs.cb_attrs[0]:
                mc.setAttr(f"{sel}.{attr}", lock=lock)
    
        if ro:
            for attr in roolibs.cb_attrs[1]:
                mc.setAttr(f"{sel}.{attr}", lock=lock)
    
        if sc:
            for attr in roolibs.cb_attrs[2]:
                mc.setAttr(f"{sel}.{attr}", lock=lock)