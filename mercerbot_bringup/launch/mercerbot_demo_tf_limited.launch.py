import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import TimerAction
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    # 1) Build robot_description from xacro
    robot_description = ParameterValue(
        Command(
            [
                "xacro ",
                os.path.join(
                    get_package_share_directory("mercerbot_description"),
                    "urdf",
                    "mercerbot.urdf.xacro",
                ),
                " is_sim:=False",
            ]
        ),
        value_type=str,
    )

    # 2) Robot State Publisher
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
        remappings=[("joint_states", "joint_states_corrected")],
        output="screen",
    )
    rviz_config_file = os.path.join(
        get_package_share_directory("mercerbot_description"),
        "rviz",
        "basic_urdf.rviz",   # or your rviz file name
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
       
        arguments=["-d", rviz_config_file],                        # RViz config
    )
  # 3) ros2_control controller manager
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": False,
            },
            os.path.join(
                get_package_share_directory("mercerbot_controller"),
                "config",
                "mercerbot_controllers.yaml",
            ),
        ],
        output="screen",
    )

    #4) Spawners (delayed so controller_manager is ready)
    joint_state_broadcaster_spawner = TimerAction(
        period=2.0,
        actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[
                    "joint_state_broadcaster",
                    "--controller-manager",
                    "/controller_manager",
                ],
                output="screen",
            )
        ],
    )

    arm_controller_spawner = TimerAction(
        period=3.0,
        actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[
                    "arm_controller",
                    "--controller-manager",
                    "/controller_manager",
                ],
                output="screen",
            )
        ],
    )

    gripper_controller_spawner = TimerAction(
        period=4.0,
        actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[
                    "gripper_controller",
                    "--controller-manager",
                    "/controller_manager",
                ],
                output="screen",
            )
        ],
    )

    slider_control_node = Node(
        package="mercerbot_controller",
        executable="slider_control"
    )

    joint_states_corrected_node = Node(
        package="mercerbot_joint_states_corrected",
        executable="joint_states_corrected_node"
    ) 
    mercerbot_joint_pub_node= Node(
        package="mercerbot_joint_pub",
        executable="joint_slider_gui"
    )

    return LaunchDescription([
        # NOTE: robot_description is NOT listed here
        robot_state_publisher_node,
        rviz_node,
        slider_control_node,
        joint_states_corrected_node,
        controller_manager,
        joint_state_broadcaster_spawner,
        arm_controller_spawner,
        gripper_controller_spawner,
        mercerbot_joint_pub_node,
       
    ])
