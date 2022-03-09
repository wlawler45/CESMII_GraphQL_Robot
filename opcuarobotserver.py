#! /usr/bin/env python3

''' Dependenices to install via pip:
      pip install pyspectator
      pip install opcua 
    Note: This generally works on Windows (including WSL) with some warnings, however pyspectator 
    requires VisualStudio C++ Build tools, and an additional Python package:
      pip install wmi
'''

from opcua import Server
#from pyspectator.processor import Cpu
#from pyspectator.computer import Computer
from random import randint
import datetime
import time
import numpy as np
from importlib import import_module
from RobotRaconteur.Client import *
import RobotRaconteurCompanion as RRC
import sys, time, yaml, traceback
sys.path.append('../toolbox/')
from general_robotics_toolbox import *    

#from abb_def import *

def connect_failed(s, client_id, url, err):
	error_msg="Client connect failed: " + str(client_id.NodeID) + " url: " + str(url) + " error: " + str(err)
	print('Reconnecting')
	fusing_obj=fusing_sub.GetDefaultClientWait(1)

if __name__ == "__main__":
    #server_url = "opc.tcp://opcua.interfacetech.cesmii.net:51210" opc.tcp://localhost:62548/Quickstarts/DataAccessServer
    server_url = "opc.tcp://localhost:62548/"
    server_name = "ROBOT_SERVER"
    sample_rate = 2

    print("Configuring Simple OPC UA Server...")
    my_ua_server = Server()
    my_ua_server.set_endpoint(server_url)

    # Register a new namespace to work in
    my_ua_namespace = my_ua_server.register_namespace(server_name)
    print("Namespace ID: {}".format(my_ua_namespace))

    # Find the "Objects" folder to attach a new object to
    my_ua_node = my_ua_server.get_objects_node()
    print("Objects Node ID: ", my_ua_node)

    # Create a new object
    my_object = my_ua_node.add_object(my_ua_namespace, "Robot 1")
    print("MyObject ID:", my_object)

    # Add some attributes (of type variable) to MyObject
    attrib_command = my_object.add_variable(my_ua_namespace, "Command Mode", 0)
    attrib_operation = my_object.add_variable(my_ua_namespace, "Operational Mode", 0)
    attrib_con_state = my_object.add_variable(my_ua_namespace, "Controller State", 0)
    attrib_joint = my_object.add_variable(my_ua_namespace, "Joint Positions", 0.0)
    attrib_effort = my_object.add_variable(my_ua_namespace, "Joint Effort", 0.0)
    attrib_velocity = my_object.add_variable(my_ua_namespace, "Joint Velocity", 0.0)
    attrib_tcp = my_object.add_variable(my_ua_namespace, "Kin chain TCP", 0.0)
    attrib_tcp_vel = my_object.add_variable(my_ua_namespace, "Kin Chain TCP vel", 0.0)
    attrib_rob_state = my_object.add_variable(my_ua_namespace, "Robot State Flag", 0)
    attrib_seqno = my_object.add_variable(my_ua_namespace, "seqno", 0)
    attrib_joint_command = my_object.add_variable(my_ua_namespace, "Joint Position Command", 0.0)
    attrib_joint_velocity = my_object.add_variable(my_ua_namespace, "Joint Velocity Command", 0.0)
    attrib_error = my_object.add_variable(my_ua_namespace, "Current Error", "System Started but Robot Raconteur Connection Not Found")
    attrib_traj_run = my_object.add_variable(my_ua_namespace, "Trajectory Running", False)


    attrib_type = my_object.add_variable(my_ua_namespace, "Robot Type Code", 0)
    attrib_capabilities = my_object.add_variable(my_ua_namespace, "Robot Capabilities", 0)
    attrib_device = my_object.add_variable(my_ua_namespace, "Device Identifier", 0)
    attrib_manufacturer = my_object.add_variable(my_ua_namespace, "Device Manufacturer", "Device Manufacturer")

    # This attribute value can be written to by a client
    #attrib_toggler = my_object.add_variable(my_ua_namespace, "Toggle Bit", False)
    #attrib_toggler.set_writable()
    RRC.RegisterStdRobDefServiceTypes(RRN)
    robosewclient='192.168.51.61'
    url='rr+tcp://'+robosewclient+':58651?service=robot'
    try:
        my_ua_server.start()
        while True:
            attrib_command.set_value(15)
            time.sleep(sample_rate)
    except KeyboardInterrupt:
        print("Press Ctrl-C to terminate while statement")
        my_ua_server.stop()
    pass
    robot_sub=RRN.SubscribeService(url)
    robot_sub.ClientConnectFailed += connect_failed
    state_w = robot_sub.SubscribeWire("robot_state")
    cmd_w = robot_sub.SubscribeWire('position_command')
    vel_w = robot_sub.SubscribeWire("velocity_command")

    robot=robot_sub.GetDefaultClientWait(1)

    #robot_const = RRN.GetConstants("com.robotraconteur.robotics.robot", robot)
    
    # state_w.WireValueChanged+=robot_state_update
    # cmd_w.WireValueChanged+=robot_command_update
    # vel_w.WireValueChanged+=robot_vel_update
    


    try:
        print()
        print("Starting Simple OPC UA Server...")
        my_ua_server.start()
        print()
        print("Generating Sample Data...")
        robot_device_info=robot.device_info
        robot_info=robot.robot_info
        attrib_type.set_value(robot_info.robot_type)
        attrib_capabilities.set_value(robot_info.robot_capabilities)
        attrib_device.set_value(robot_device_info.device.name)
        attrib_manufacturer.set_value(robot_device_info.manufacturer.name)
        
        

        while True:
            #Update the attribute values for my object
            attrib_command.set_value(robot.command_mode)
            attrib_operation.set_value(robot.operational_mode)
            attrib_con_state.set_value(robot.controller_state)
            
            #####attrib_error
            
            robot_state=state_w.InValue
            attrib_seqno.set_value(robot_state.seqno)
            attrib_rob_state.set_value(robot_state.robot_state_flags)
            attrib_joint.set_value(robot_state.joint_position)
            attrib_effort.set_value(robot_state.joint_effort)
            attrib_velocity.set_value(robot_state.joint_velocity)
            #attrib_tcp.set_value(robot_state.kin_chain_tcp)
            #attrib_tcp_vel.set_value(robot_state.kin_chain_tcp_vel
            attrib_traj_run.set_value(robot_state.trajectory_running)
            
            
            
            joint_command=cmd_w.InValue.command
            attrib_joint_command.set_value(joint_command)
            
            vel_command=vel_w.InValue.command
            attrib_joint_velocity.set_value(vel_command)
            #attrib_joint.set_value(joints)
            #attrib_press.set_value(computer.virtual_memory.used_percent)

            print ("Current values: ", attrib_joint.get_value())

            time.sleep(sample_rate)
    finally:
        my_ua_server.stop()
        print("Server Offline")

# def robot_state_update(w,value,time):
    # val=w.InValue
    # #joints=[0.0,0.0,1.0,4.0]
    
    # attrib_seqno.set_value(70)
    # attrib_rob_state
    # attrib_joint
    # attrib_effort
    # attrib_velocity
    # attrib_tcp
    # attrib_tcp_vel
    # attrib_traj_run
    # #attrib_joint.set_value(joints)
    # print (val.seqno)
    
# def robot_command_update(w,value,time):
    # val=w.InValue
    # attrib_joint_command
    # #Print the new value to the console.  Comment out this line
    # #to see the other output more clearly
    # print (val.seqno)

# def robot_vel_update(w,value,time):
    # val=w.InValue
    # attrib_joint_velocity
    # #Print the new value to the console.  Comment out this line
    # #to see the other output more clearly
    # print (val.seqno)
    
