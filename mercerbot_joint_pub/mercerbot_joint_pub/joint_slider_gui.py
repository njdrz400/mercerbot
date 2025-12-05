#!/usr/bin/env python3
import math
import tkinter as tk

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class JointSliderGui(Node):
    def __init__(self):
        super().__init__("joint_slider_gui")

        self.pub = self.create_publisher(JointState, "joint_states", 10)

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

            slider = tk.Scale(
                frame,
                from_=-math.pi/2.0,
                to=math.pi/2.0,
                resolution=0.01,
                orient=tk.HORIZONTAL,
                length=400,
                command=self.on_slider_move
            )
            if joint == "joint_4":
                slider = tk.Scale(
                    frame,
                    from_=-math.pi/2.0,
                    to=0,
                    resolution=0.01,
                    orient=tk.HORIZONTAL,
                    length=400,
                    command=self.on_slider_move
                )
         

               

            slider.set(0.0)
            slider.pack()

            self.sliders[joint] = slider

        # Close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_slider_move(self, _value):
        """Any slider moves = publish new joint state."""
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = []
        msg.position = []

        for joint in self.joints:
            msg.name.append(joint)
            msg.position.append(float(self.sliders[joint].get()))

        msg.name.append("joint_3_corrected")
        msg.position.append(float(self.sliders["joint_3"].get()) - float(self.sliders["joint_2"].get()))
        #self.get_logger().debug("Publishing joint_3_corrected: {:.2f}".format(float(self.sliders["joint_2"].get())))
        print(self.sliders["joint_3"].get(),self.sliders["joint_2"].get())
        msg.name.append("joint_claw_support_corrected")
        msg.position.append(3.14/2.0-float(self.sliders["joint_3"].get()))


        self.pub.publish(msg)

    def on_close(self):
        self.get_logger().info("Closing GUI...")
        rclpy.shutdown()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def main(args=None):
    rclpy.init(args=args)
    node = JointSliderGui()
    node.run()


if __name__ == "__main__":
    main()
