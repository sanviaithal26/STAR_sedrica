#!/usr/bin/env python3
# A simple ROS2 Subscriber

import rclpy 
from rclpy.node import Node

from nav_msgs.msg import Odometry
from math import atan2

class OdomSubscriber(Node): 

    def __init__(self): 
        super().__init__("odom_subscriber") 

        self.my_subscriber = self.create_subscription(
            msg_type=Odometry,
            topic="/odom",
            callback=self.msg_callback,
            qos_profile=10,
        ) 

        self.get_logger().info(
            f"The '{self.get_name()}' node is initialised."
        ) 

        self.counter = 0

    def msg_callback(self, topic_message: Odometry): 

        pose = topic_message.pose.pose 

        pos_x = pose.position.x
        pos_y = pose.position.y
        pos_z = pose.position.z

        yaw = self.quaternion_to_euler(pose.orientation) 

        if self.counter > 10: 
            self.counter = 0
            self.get_logger().info(
                f"x = {pos_x:.3f} (m), y = ? (m), yaw = ? (radians)"
            ) 
        else:
            self.counter += 1

    def quaternion_to_euler(self, orientation):
        x = orientation.x
        y = orientation.y
        z = orientation.z
        w = orientation.w

        yaw = atan2(2*(w*y + x*z), 1-2*(y*y+z*z))
        return yaw # (in radians)

def main(args=None): 
    rclpy.init(args=args)
    my_odom_subscriber = OdomSubscriber()
    rclpy.spin(my_odom_subscriber)
    my_odom_subscriber.destroy_node()
    rclpy.shutdown() 

if __name__ == '__main__':
    main()