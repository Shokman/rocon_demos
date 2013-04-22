#! /usr/bin/env python

import roslib; roslib.load_manifest('cafe_msgs')
import rospy

# Brings in the SimpleActionClient
import actionlib

# Brings in the messages used by the deliver order action, including the
# goal message and the result message.
import cafe_msgs.msg

def deliver_order_client():
    # Creates the SimpleActionClient, passing the type of the action
    # (DeliverOrderAction) to the constructor.
    client = actionlib.SimpleActionClient('deliver_order', cafe_msgs.msg.DeliverOrderAction)

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()

    # Creates a goal to send to the action server.
    goal = cafe_msgs.msg.DeliverOrderGoal()
    table_id = rospy.get_param("~table_id", 0)
    order_id = rospy.get_param("~order_id", 0)
    goal.order.table_id = table_id
    goal.order.order_id = order_id
    print "Deliver order ", order_id, " to table ", table_id

    # Sends the goal to the action server.
    client.send_goal(goal)

    # Waits for the server to finish performing the action.
    client.wait_for_result()

    # Prints out the result of executing the action
    return client.get_result()  # A DeliverOrderResult

if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('deliver_order_client')
        result = deliver_order_client()
        print "Result:", result.result
    except rospy.ROSInterruptException:
        print "program interrupted before completion"