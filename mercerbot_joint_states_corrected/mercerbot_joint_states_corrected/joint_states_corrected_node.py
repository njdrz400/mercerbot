#!/usr/bin/env python3
import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class CorrectedJointState(Node):
    def __init__(self):
        super().__init__("corrected_joint_state")

        self.sub = self.create_subscription(
            JointState,
            "/joint_states",
            self.cb,
            10,
        )

        self.pub = self.create_publisher(
            JointState,
            "/joint_states_corrected",
            10,
        )

    def cb(self, msg: JointState):
        # Copy original joint state
        out = JointState()
        out.header = msg.header
        out.name = list(msg.name)
        out.position = list(msg.position)
        out.velocity = list(msg.velocity) if msg.velocity else []
        out.effort = list(msg.effort) if msg.effort else []

        # Get indices of real joints
        try:
            i2 = msg.name.index("joint_2")
            i3 = msg.name.index("joint_3")
        except ValueError:
            # If joints not present yet, skip
            return

        q2 = msg.position[i2]
        q3 = msg.position[i3]

        # Add fake joints
        out.name.append("joint_3_corrected")
        out.position.append(q3 - q2)

        out.name.append("joint_claw_support_corrected")
        out.position.append(math.pi / 2.0 - q3)

        self.pub.publish(out)


def main(args=None):
    rclpy.init(args=args)
    node = CorrectedJointState()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
