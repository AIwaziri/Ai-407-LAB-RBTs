import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import numpy as np

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10)
        self.cmd = Twist()  # movement command

    def lidar_callback(self, msg):
        # convert ranges to a NumPy array for easier handling.
        ranges = np.array(msg.ranges)

        # this to define how many readings on each end to consider as the "front."
        front_window = 15  

        # For sensors with angle_min = 0.0 and angle_max ≈ 6.28, the front might be at 0°.
        # So, we take the first and last few readings to form a continuous front window.
        front_ranges = np.concatenate((ranges[:front_window], ranges[-front_window:]))

        # Filter out invalid readings: ignore zeros and infinities.
        valid_ranges = front_ranges[(front_ranges > msg.range_min) & np.isfinite(front_ranges)]
        if valid_ranges.size == 0:
            min_front_distance = float('inf')
        else:
            min_front_distance = np.min(valid_ranges)

        self.get_logger().info(f'Front Distance: {min_front_distance:.2f} meters')

        # Only if an obstacle is detected within 0.5m in the front area, avoid it.
        if min_front_distance < 0.5:
            self.avoid_obstacle()
        else:
            self.move_forward()

        self.publisher.publish(self.cmd)

    def move_forward(self):
        self.cmd.linear.x = 0.2 # move forward
        self.cmd.angular.z = 0.0 # no turn

    def avoid_obstacle(self):
        self.get_logger().warn('Obstacle detected in front! Turning...')
        self.cmd.linear.x = 0.0   # stop forward
        self.cmd.angular.z = 0.5  # turn 

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidance()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
