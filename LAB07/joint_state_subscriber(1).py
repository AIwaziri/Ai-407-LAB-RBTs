import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import time

class JointStateSubscriber(Node):
    def __init__(self):
        super().__init__('joint_state_subscriber')

        # Create a subscriber to the /joint_states topic
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_states_callback,
            10
        )

        self.get_logger().info("Subscribed to /joint_states")

    def joint_states_callback(self, msg):
        self.get_logger().info(f"Received joint states: {msg.position}")
        time.sleep(2)

def main(args=None):
    rclpy.init(args=args)  
    node = JointStateSubscriber()  
    rclpy.spin(node)  
    node.destroy_node()  
    rclpy.shutdown()  

if __name__ == '__main__':
    main()

