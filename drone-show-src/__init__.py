import bpy

bl_info = {
    "name": "Drone show animation (.csv)",
    "author": "Artem Vasiunik & Arthur Golubtsov",
    "version": (1, 4, 0),
    "blender": (3, 2, 2),
    "location": "File > Export > Drone show animation (.csv)",
    "description": "Export > Drone show animation (.csv)",
    "doc_url": "https://github.com/DroneLegion/BlenderDroneShow/blob/master/README.md",
    "tracker_url": "https://github.com/DroneLegion/BlenderDroneShow/issues",
    "category": "Import-Export",
}

from . import operators, ui
from .properties import (
    DroneLedProperties,
    DroneObjectProperties,
    DroneShowProperties,
)

classes = (
    DroneShowProperties,
    DroneObjectProperties,
    DroneLedProperties,
    operators.ExportAnimation,
    #operators.ExportAnimationChecksPanel,
    #operators.CheckSwarmAnimation,
    operators.AssignDrones,
    operators.SelectDrones,
    #operators.SetLedColor,
    #operators.SetLedRainbow,
    ui.DronePanel,
    ui.DroneCoordsPanel,
    ui.DroneLedPanel,
    ui.LedPanel,
    ui.DroneOperatorsPanel,
    #ui.LedOperatorsPanel,
    ui.AnimationPanel,
    ui.AddMenu,
)


def export_animation_menu(self, context):
    self.layout.operator(
        operators.ExportAnimation.bl_idname, text="Drone show animation (.csv)"
    )




def add_menu(self, context):
    self.layout.menu(self.layout.menu(ui.AddMenu.bl_idname))


# noinspection PyNoneFunctionAssignment


# noinspection PyNoneFunctionAssignment
def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.types.Scene.drone_show = bpy.props.PointerProperty(type=DroneShowProperties)

    bpy.types.Object.drone = bpy.props.PointerProperty(type=DroneObjectProperties)
    # bpy.types.Material.led = bpy.props.PointerProperty(type=DroneLedProperties)

    bpy.types.TOPBAR_MT_file_export.append(export_animation_menu)

    bpy.types.VIEW3D_MT_add.append(add_menu)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.drone_show

    del bpy.types.Object.drone
    del bpy.types.Material.led



    bpy.types.TOPBAR_MT_file_export.remove(export_animation_menu)

    bpy.types.VIEW3D_MT_add.remove(add_menu)


if __name__ == "__main__":
    register()
