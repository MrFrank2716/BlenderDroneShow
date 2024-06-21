import os
import bpy
import csv
import sys
from bpy.types import Operator
from bpy.props import BoolProperty
from bpy_extras.io_utils import ExportHelper
from bpy_extras.io_utils import ImportHelper

from sbstudio.plugin.props.frame_range import FrameRangeProperty
from sbstudio.plugin.operators import utils as sbs_pl_op_utils
from sbstudio.plugin import errors as sbs_pl_errors



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

        # try:
        export_selected_only = self.export_selected
        drones = list(sbs_pl_op_utils.get_drones_to_export(selected_only=export_selected_only))
        if not drones:
            if export_selected_only:
                raise sbs_pl_errors.SkybrushStudioExportWarning(
                    "No objects were selected; export cancelled"
                )
            else:
                raise sbs_pl_errors.SkybrushStudioExportWarning(
                    "There are no objects to export; export cancelled"
                )
        (
            trajectories,
            lights,
        ) = sbs_pl_op_utils._get_trajectories_and_lights(drones, settings, frame_range, context=context)

        self.report({"INFO"}, "Export started")

        def format_drone(name: str):
            settings = {
                "name": name,
                "lights": lights[name].as_dict(ndigits=3),
                "trajectory": trajectories[name].as_dict(ndigits=3, version=0),
            }

            # Frank: Retrieve the actual Blender object
            drone_obj = bpy.data.objects[name]

            # Create a CSV file for each drone
            with open(os.path.join(os.path.dirname(self.filepath), f"{name}.csv"), 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Time [msec]", "x [m]", "y [m]", "z [m]", "Red", "Green", "Blue"])

                fps = bpy.context.scene.render.fps # Frank: Getting the projects scene FPS

                # Frank: Determine the total time of the animation in milliseconds
                total_time_ms = ((bpy.context.scene.frame_end / fps) * 1000)

                # Frank: Calculate the number of 250ms intervals in the total time
                num_intervals = int(total_time_ms // 250)

                # Frank: Loop over each 250ms interval
                for i in range(num_intervals):
                    # Frank: Calculate the time for this interval
                    time_ms = i * 250

                    # Frank: Calculate the equivalent frame for this time
                    frame = (time_ms / 1000) * fps

                    # Frank: Set the scene to this frame
                    bpy.context.scene.frame_set(round(frame))

                    # Frank: Get drone location from the actual Blender object
                    loc = drone_obj.matrix_world.translation
                    loc = [round(l, 3) for l in loc]

                    # Frank: Get drone color from the actual Blender object by looking at it's node tree
                    if drone_obj.data.materials:
                        mat = drone_obj.data.materials[0]
                        if 'Emission' in mat.node_tree.nodes:
                            col = mat.node_tree.nodes['Emission'].inputs[0].default_value
                        else:
                            col = [1, 1, 1, 1]
                    else:
                        col = [1, 1, 1, 1]

                    # Frank: Converting to RGB Values
                    col_rgb = [round(c * 255) for c in col[:3]]

                    writer.writerow([time_ms, loc[0], loc[1], loc[2]] + col_rgb)

        # Get start and end drone indices from command line arguments
        args = sys.argv[sys.argv.index("--") + 1:]  # get all args after "--"
        start_drone = int(args[0])
        end_drone = int(args[1])
        # Only process drones within the specified range
        for drone in drones[start_drone - 1:end_drone]:
            format_drone(drone.name)

        self.report({"INFO"}, "Export successful")
        return {"FINISHED"}


