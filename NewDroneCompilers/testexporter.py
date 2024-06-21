bl_info = {
    "name" : "mcparks_skybrush_exporter",
    "author" : "Lumi Chroma & Frank (ThunderMesa)",
    "description" : "Exports Skybrush Studio drone animations to a .csv format for MCParks",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 4),
    "location" : "",
    "warning" : "",
    "category" : "Import-Export"
}

import os
import bpy
import csv
from bpy.types import Operator
from bpy.props import BoolProperty
from bpy_extras.io_utils import ExportHelper
from bpy_extras.io_utils import ImportHelper

from sbstudio.plugin.props.frame_range import FrameRangeProperty
from sbstudio.plugin.operators import utils as sbs_pl_op_utils
from sbstudio.plugin import errors as sbs_pl_errors

def create_mesh_from_png(image_path):
    img = bpy.data.images.load(image_path)
    width, height = img.size

    bpy.ops.mesh.primitive_uv_sphere_add()
    obj = bpy.context.active_object
    me = obj.data

    me.clear_geometry()

    verts = [(x, y, 0) for x in range(width) for y in range(height) if img.pixels[(y * width + x) * 4] < 0.5]
    me.from_pydata(verts, [], [])
    me.update()

class ImportPNG(Operator, ImportHelper):
    bl_idname = "import.png"
    bl_label = "Import PNG"

    filter_glob: bpy.props.StringProperty(
        default="*.png",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        create_mesh_from_png(self.filepath)
        return {'FINISHED'}

class MCParksPanel(bpy.types.Panel):
    bl_label = "MCParks Panel"
    bl_idname = "MCPARKS_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MCParks"

    def draw(self, context):
        layout = self.layout
        layout.operator("import.png")
class ExportMCParksOperator(Operator, ExportHelper):
    bl_idname = "object.exportmcparks"
    bl_label = "ExportMCParks"
    filename_ext = ".csv"

    export_selected: BoolProperty(
        name="Export selected drones only",
        default=False,
        description=(
            "Export only the selected drones. "
            "Uncheck to export all drones, irrespectively of the selection."
        ),
    )

    # frame range
    frame_range: FrameRangeProperty(default="RENDER")

    # def execute(self, context):
    #     return {'FINISHED'}

    def execute(self, context):
        filepath = bpy.path.ensure_ext(self.filepath, self.filename_ext)

        if os.path.basename(filepath).lower() == self.filename_ext.lower():
            self.report({"ERROR_INVALID_INPUT"}, "Filename must not be empty")
            return {"CANCELLED"}

        settings = {
            "export_selected": self.export_selected,
            "frame_range": self.frame_range,
            "min_nav_altitude": 0.1,  # TODO(ntamas): should be configurable,
            "output_fps": 20,
            "light_output_fps": 20,
        }
        frame_range = sbs_pl_op_utils.resolve_frame_range(settings['frame_range'], context=context)

        drones = list(sbs_pl_op_utils.get_drones_to_export(selected_only=self.export_selected))
        if not drones:
            if self.export_selected:
                raise sbs_pl_errors.SkybrushStudioExportWarning("No objects were selected; export cancelled")
            else:
                raise sbs_pl_errors.SkybrushStudioExportWarning("There are no objects to export; export cancelled")

        trajectories, lights = sbs_pl_op_utils._get_trajectories_and_lights(drones, settings, frame_range,
                                                                            context=context)

        self.report({"INFO"}, "Export started")

        fps = bpy.context.scene.render.fps
        total_time_ms = ((bpy.context.scene.frame_end / fps) * 1000)
        num_intervals = int(total_time_ms // 250)

        drone_data = []
        for drone in drones:
            drone_name = drone.name
            drone_obj = bpy.data.objects[drone_name]

            rows = []
            for i in range(num_intervals):
                time_ms = i * 250
                frame = (time_ms / 1000) * fps
                bpy.context.scene.frame_set(round(frame))

                loc = drone_obj.matrix_world.translation
                loc = [int(l * 1000) / 1000 for l in loc]

                if drone_obj.data.materials:
                    mat = drone_obj.data.materials[0]
                    if 'Emission' in mat.node_tree.nodes:
                        col = mat.node_tree.nodes['Emission'].inputs[0].default_value
                    else:
                        col = [1, 1, 1, 1]
                else:
                    col = [1, 1, 1, 1]

                col_rgb = [int(c * 255) for c in col[:3]]

                rows.append([time_ms, loc[0], loc[1], loc[2]] + col_rgb)

            drone_data.append(rows)

        for i, drone in enumerate(drones):
            with open(os.path.join(os.path.dirname(filepath), f"{drone.name}.csv"), 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Time [msec]", "x [m]", "y [m]", "z [m]", "Red", "Green", "Blue"])
                writer.writerows(drone_data[i])

        self.report({"INFO"}, "Export successful")
        return {"FINISHED"}


def register():
    print('register')
    bpy.utils.register_class(ImportPNG)
    bpy.utils.register_class(MCParksPanel)
    bpy.utils.register_class(ExportMCParksOperator)
    def export_func(self, context):
        self.layout.operator("object.exportmcparks", text="Export to MCParks (.csv)")
    bpy.types.OBJECT_PT_skybrush_export_panel.append(export_func)

def unregister():
    print('unregister')
    bpy.utils.unregister_class(ImportPNG)
    bpy.utils.unregister_class(MCParksPanel)
    bpy.utils.unregister_class(ExportMCParksOperator)
    bpy.utils.OBJECT_PT_skybrush_export_panel.remove(export_func) # Frank: Added this so it removes the button in the panel on unregister.

if __name__ == "__main__":
    register()
    import bpy.ops
    bpy.ops.object.exportmcparks('EXEC_DEFAULT', filepath="/Users/pearl/dump.csv", frame_range="RENDER")