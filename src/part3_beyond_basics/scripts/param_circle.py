#!/usr/bin/env python3
# A simple ROS2 Publisher

import rclpy 
from rclpy.node import Node

from geometry_msgs.msg import Twist
from rclpy.signals import SignalHandlerOptions

class Circle(Node): 

    def __init__(self):
        super().__init__("param_circle") 

        self.declare_parameter(
        name="radius", 
        value=0.5 # meters
        )

        self.my_publisher = self.create_publisher(
            msg_type=Twist,
            topic="/cmd_vel",
            qos_profile=10,
        ) 

        publish_rate = 10 # Hz
        self.timer = self.create_timer(
            timer_period_sec=1/publish_rate, 
            callback=self.timer_callback
        ) 

        self.get_logger().info(
            f"The '{self.get_name()}' node is initialised." 
        )

        self.shutdown = False

    def timer_callback(self):
        radius = self.get_parameter("radius").get_parameter_value().double_value
        linear_velocity = 0.1 # meters per second [m/s]
        angular_velocity = linear_velocity/radius

        topic_msg = Twist() 
        topic_msg.linear.x = linear_velocity
        topic_msg.angular.z = angular_velocity
        self.my_publisher.publish(topic_msg) 

        self.get_logger().info( 
            f"Moving with radius: {radius:.2f} [m]\n"
            f"Linear Velocity: {topic_msg.linear.x:.2f} [m/s], "
            f"Angular Velocity: {topic_msg.angular.z:.2f} [rad/s].",
            throttle_duration_sec=1, 
        )

    def on_shutdown(self):
        self.get_logger().info(
            "Stopping the robot..."
        )
        self.my_publisher.publish(Twist()) 
        self.shutdown = True
        
def main(args=None):
    rclpy.init(
        args=args,
        signal_handler_options=SignalHandlerOptions.NO
    ) 
    move_circle = Circle()
    try:
        rclpy.spin(move_circle) 
    except KeyboardInterrupt: 
        print(
            f"{move_circle.get_name()} received a shutdown request (Ctrl+C)."
        )
    finally: 
        move_circle.on_shutdown() 
        while not move_circle.shutdown: 
            continue
        move_circle.destroy_node() 
        rclpy.shutdown()

if __name__ == '__main__': 
    main()