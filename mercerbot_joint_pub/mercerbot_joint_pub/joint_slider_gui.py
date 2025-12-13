#!/usr/bin/env python3
import math
import tkinter as tk

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class JointSliderGui(Node):
    def __init__(self):
        super().__init__("joint_slider_gui")

        self.pub = self.create_publisher(JointState, "joint_commands", 10)

        # Tkinter GUI
        self.root = tk.Tk()
        self.root.title("Joint State GUI")

        # Joint names
        self.joints = ["joint_1", "joint_2", "joint_3", "joint_4"]

        # Store slider widgets so we can read their values each publish
        self.sliders = {}

        # Build GUI
        for joint in self.joints:
            frame = tk.Frame(self.root)
            frame.pack(padx=10, pady=5)

            label = tk.Label(frame, text=f"{joint} (rad)")
            label.pack()

            # Default range: [-pi/2, pi/2]
            from_val = -math.pi / 2.0
            to_val = math.pi / 2.0

            # Special range for joint_4: [-pi/2, 0]
            if joint == "joint_4":
                to_val = 0.0
                from_val = -math.pi / 2.0

            slider = tk.Scale(
                frame,
                from_=from_val,
                to=to_val,
                resolution=0.01,
                orient=tk.HORIZONTAL,
                length=400,
                command=self.on_slider_move,  # Tk passes the value as a string
            )

            slider.set(0.0)
            slider.pack()

            self.sliders[joint] = slider

        # Close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_slider_move(self, _value=None):
        """Any slider moves = publish new joint state."""
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = []
        msg.position = []

        # Base joints
        for joint in self.joints:
            msg.name.append(joint)
            msg.position.append(float(self.sliders[joint].get()))

        # Derived joints
        joint_2_val = float(self.sliders["joint_2"].get())
        joint_3_val = float(self.sliders["joint_3"].get())

        # joint_3_corrected = joint_3 - joint_2
        #msg.name.append("joint_3_corrected")
        #msg.position.append(joint_3_val - joint_2_val)

        # joint_claw_support_corrected = pi/2 - joint_3
        #msg.name.append("joint_claw_support_corrected")
        #msg.position.append(math.pi / 2.0 - joint_3_val)

        self.pub.publish(msg)

    def on_close(self):
        self.get_logger().info("Closing GUI...")
        # Clean up ROS and Tk
        self.destroy_node()
        rclpy.shutdown()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def main(args=None):
    rclpy.init(args=args)
    node = JointSliderGui()
    try:
        node.run()
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == "__main__":
    main()
