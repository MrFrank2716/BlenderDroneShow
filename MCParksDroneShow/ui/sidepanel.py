from bpy.types import Panel

# from .checks import draw_check_properties

__all__ = ("DroneOperatorsPanel", "LedOperatorsPanel", "AnimationPanel")


class DroneOperatorsPanel(Panel):
    bl_idname = "VIEW3D_PT_drone"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MCParks"
    bl_label = "Drones Functions"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.operator("drone_show.assign")
        col.operator("drone_show.select")


# class LedOperatorsPanel(Panel):
#     bl_idname = "VIEW3D_PT_led"
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_category = "Drone show"
#     bl_label = "LEDs operators"

#     def draw(self, context):
#         layout = self.layout
#         drone_show = context.scene.drone_show

#         col = layout.column(align=True)
#         col.prop(drone_show, "led_color", text="")
#         col.operator("drone_show.set_leds")

#         col = layout.column(align=True)
#         col.operator("drone_show.set_leds_rainbow")


class AnimationPanel(Panel):
    bl_idname = "VIEW3D_PT_animation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MCParks"
    bl_label = "Export"

    def draw(self, context):
        layout = self.layout
        drone_show = context.scene.drone_show

        # draw_check_properties(drone_show, layout)

        layout.separator()

        col = layout.column(align=True)
        # col.operator("drone_show.check")
        col.operator("drone_show.export_animation")

