import rclpy
import time
from rclpy.node import Node

from std_msgs.msg import String
from dh_gripper_ros2.msg import GripperCtrl
from dh_gripper_ros2.msg import GripperState #sub
# ?=

class GripperController(Node):

    timer_period = 0.005  # seconds
    i = 0
    state = 0
    isReset = False

    m_position = 0
    m_target_position = 0
    m_target_force = 0

    def __init__(self):
        super().__init__('gripper_controller')
        self.timer = self.create_timer(self.timer_period, self.gripper_control)
        # Publisher
        self.gripper_ctrl_pub = self.create_publisher(GripperCtrl, "/gripper/ctrl", 10)
        # Subscriber
        self.gripper_state_sub = self.create_subscription(GripperState, '/gripper/states', self.gripper_callback, 10) 
        self.gripper_state_sub
        self.gripper_cmd_sub = self.create_subscription(String, 'gripper_cmd', self.gripper_cmd_callback, 10)
        self.gripper_cmd_sub

    def gripper_control(self):
        msg_ctrl_msg = GripperCtrl()
        if(self.isReset):
            msg_ctrl_msg.initialize = True
            msg_ctrl_msg.position = 0.0
            msg_ctrl_msg.force = 0.0
            msg_ctrl_msg.speed = 0.0
            self.isReset = True
        else:
            match self.state:
                # Fully open
                case 0:
                    msg_ctrl_msg.initialize = False
                    msg_ctrl_msg.position = 1000.0
                    msg_ctrl_msg.force = 1000.0
                    msg_ctrl_msg.speed = 5.0
                # 50% open
                case 1:
                    msg_ctrl_msg.initialize = False
                    msg_ctrl_msg.position = 650.0
                    msg_ctrl_msg.force = 200.0
                    msg_ctrl_msg.speed = 5.0
                # Fully close
                case 2:
                    msg_ctrl_msg.initialize = False
                    msg_ctrl_msg.position = 0.0
                    msg_ctrl_msg.force = 200.0
                    msg_ctrl_msg.speed = 5.0
        self.gripper_ctrl_pub.publish(msg_ctrl_msg)

    
    def gripper_callback(self, msgs):    #sub
        self.m_position = msgs.position
        self.m_target_position = msgs.target_position
        self.m_target_force = msgs.target_force
        # self.get_logger().info(f"Position = {self.m_position}")
        # self.get_logger().info(f"Target position = {self.m_target_position}")
        # self.get_logger().info(f"Target force = {self.m_target_force}")

    def gripper_cmd_callback(self, msgs):
        self.state = int(msgs.data)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = GripperController()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()