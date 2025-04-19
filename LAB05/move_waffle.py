import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleController(Node):
	def __init__(self):
		super().__init__('turtle_controller')
		self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
		self.timer = self.create_timer(1.0, self.move_turtle)
		
	def move_turtle(self):
		msg = Twist()
		msg.linear.x = 1.0 # Move forward
		msg.angular.z = 1.0 # Rotate Left
		self.publisher_.publish(msg)
		self.get_logger().info(f'Publishing linear.x={msg.linear.x}, angular.z={msg.angular.z}')
		
def main(args=None):
	rclpy.init(args=args)
	node = TurtleController()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()
	
if __name__ == '__main__':
	main()
