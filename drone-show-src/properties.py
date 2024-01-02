import bpy
from bpy.types import PropertyGroup

class DroneShowProperties(PropertyGroup):
    # Check properties
    # check_led: bpy.props.BoolProperty(
    #     name="Check LEDs",
    #     description="Check LEDs material on drones",
    #     default=False,
    #     options=set(),
    # )

    # check_speed: bpy.props.BoolProperty(
    #     name="Check speed",
    #     description="Check maximum drone movement speed",
    #     default=False,
    #     options=set(),
    # )

    # speed_limit: bpy.props.FloatProperty(
    #     name="Speed limit",
    #     description="Limit of maximum drone movement speed (m/s)",
    #     unit="VELOCITY",
    #     default=3,
    #     min=0,
    #     soft_min=0.5,
    #     soft_max=20,
    #     step=50,
    # )

    # check_distance: bpy.props.BoolProperty(
    #     name="Check distance",
    #     description="Check distance between drones",
    #     default=False,
    #     options=set(),
    # )

    # distance_limit: bpy.props.FloatProperty(
    #     name="Distance limit",
    #     description="Closest possible distance between drones (m)",
    #     unit="LENGTH",
    #     default=1.5,
    #     min=0,
    #     soft_min=0.5,
    #     soft_max=10,
    #     step=50,
    # )

    # detailed_warnings: bpy.props.BoolProperty(
    #     name="Show detailed warnings",
    #     description="Show detailed animation check warnings",
    #     default=True,
    #     options=set(),
    # )

    # Led properties
    led_color: bpy.props.FloatVectorProperty(
        name="LED color",
        description="Color of the LED to set",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 1.0),
    )


class DroneObjectProperties(PropertyGroup):
    is_drone: bpy.props.BoolProperty(
        name="Is drone",
        default=False,
        options=set(),
    )


class DroneLedProperties(PropertyGroup):
    is_led: bpy.props.BoolProperty(
        name="Is LED color",
        default=True,
        options=set(),
    )
