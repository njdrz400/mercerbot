import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    mercerbot_description_dir = get_package_share_directory("mercerbot_description")






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
        output="screen",
    )
   

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
       
    )

   
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", os.path.join(mercerbot_description_dir, "rviz", "display.rviz")],
    )
    return LaunchDescription([
        #robot_description,
  
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node,
    ])