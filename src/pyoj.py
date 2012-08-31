#!/usr/bin/env python
import roslib; roslib.load_manifest('pyoj')

import rospy
import tf

import SocketServer
import math

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

PORTNO = 10552

class handler(SocketServer.DatagramRequestHandler):
    def handle(self):
        newmsg = self.rfile.readline().rstrip()
        print "Client %s said ``%s''" % (self.client_address[0], newmsg)
        self.wfile.write(self.server.oldmsg)
        self.server.oldmsg = newmsg
        args = newmsg.split(',')
        x = -float(args[2])
        y = float(args[3])
        z = float(args[4])
        d = math.sin(math.radians(5))
        
        if abs(x) < d:
          x = 0
        else:
          x -= x/math.fabs(x)*d
        
        if abs(z) < d:
          z = 0
        else:
          z -= z/math.fabs(z)*d
        
        k = 1 / math.cos(math.radians(60))
        pub.publish(Joy(axes=[1.5*k*z, 0.0, 0.0, k*x], buttons=[1] ))
        #pub_tf.sendTransform((x,y,z),tf.transformations.quaternion_from_euler(0,0,0),rospy.Time.now(), "acc_link", "base_link")
        cmd = Twist()
        cmd.linear.x=-k*z/2
        cmd.angular.z=k*x/2
        pub_cv.publish(cmd)

pub = rospy.Publisher('joy', Joy)
#pub_tf = tf.TransformBroadcaster()
pub_cv = rospy.Publisher('cmd_vel', Twist)
rospy.init_node('pyoj', anonymous=True)
s = SocketServer.UDPServer(('',PORTNO), handler)
print "Awaiting UDP messages on port %d" % PORTNO
s.oldmsg = "This is the starting message."
s.serve_forever()

