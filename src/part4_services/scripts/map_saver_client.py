#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from nav2_msgs.srv import SaveMap

class MapSaverClient(Node):

    def __init__(self):
        super().__init__('map_saver_client')

        self.client = self.create_client(
            srv_type=SaveMap, 
            srv_name='/map_saver/save_map'
        ) 

        self.declare_parameters(
            namespace='',
            parameters=[
                ('map_file', 'my_default_map')
            ]
        ) 

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                "Waiting for service..."
            ) 

    def send_request(self): 
        map_file_input = self.get_parameter(
            'map_file' 
        ).get_parameter_value().string_value 

        self.get_logger().info(
            f"Sending the request:\n"
            f" - map_topic: /map\n"
            f" - map_url: {map_file_input}\n"
            f"   Awaiting response..."
        ) 

        request = SaveMap.Request() 
        request.map_topic = '/map'
        request.map_url = map_file_input

        return self.client.call_async(request)

def main():
    rclpy.init()
    client = MapSaverClient()

    future = client.send_request() 
    rclpy.spin_until_future_complete(client, future) 
    response = future.result() 

    if response.result:
        client.get_logger().info("Success! The map was saved.")
    else:
        client.get_logger().error("The map server failed to save the map.")

    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()