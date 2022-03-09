#! /usr/bin/env python3

''' Dependenices to install via pip:
      pip install pyspectator
      pip install opcua 
    Note: This generally works on Windows (including WSL) with some warnings, however pyspectator 
    requires VisualStudio C++ Build tools, and an additional Python package:
      pip install wmi
'''

import argparse
import requests
import json

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
from datetime import datetime
#from abb_def import *

def connect_failed(s, client_id, url, err):
	error_msg="Client connect failed: " + str(client_id.NodeID) + " url: " + str(url) + " error: " + str(err)
	print('Reconnecting')
	fusing_obj=fusing_sub.GetDefaultClientWait(1)
    
class GraphQL_sender:
    def __init__(self, args,token):
        self.current_bearer_token=token
        self.args=args
        self.robot=None
        self.ID_Dict={"JointEffort":466,"KinChainTCPVel":467,"IsRunning":465,"KinChainTCP":472,"ControllerState":468,"JointVelocityCommand":469,"RobotCapabilities":470,"JointPositions":471,"CommandMode":473,"seqno":474,"CurrentError":475,"DeviceIdentifier":476,"JointVelocity":477,"OperationalMode":478,"RobotStateFlag":479,"JointPositionCommand":480,"RobotTypeCode":481,"DeviceManufacturer":482}
        #bearer=self.get_bearer_token()
        #print(bearer)
        #self.send_initial_robot_data(88,1)
        
    
    
    def assign_RR_robot(self,RR_robot_interface):
        self.robot=RR_robot_interface
    ''' Forms and sends a GraphQL request (query or mutation) and returns the response
    Accepts: The JSON payload you want to send to GraphQL and post arguments established above
    Returns: The JSON payload returned from the Server '''
    
    
    def convert_array_to_string(self, array):
        starting_string="["
        for i in range(len(array)):
            starting_string+=(str(array[i]))
            starting_string+=(",")
        
        output_string=starting_string[:-1]
        output_string+="]"
        print(output_string)
        return output_string
        
    def send_initial_robot_data(self,robot_info,device_info):
        #attrib_type.set_value(robot_info.robot_type)
        # attrib_capabilities.set_value(robot_info.robot_capabilities)
        # attrib_device.set_value(robot_device_info.device.name)
        # attrib_manufacturer.set_value(robot_device_info.manufacturer.name)
        #now=datetime.now()
        #timesta=now.strftime("%Y-%m-%dT%H:%M:%SZ")
        #startTime=now.strftime("%Y-%m-%d")
        #EndTime=now.strftime("%Y-%m-05")
        smp_query = """ 
            mutation MyMutation4 {
              updateAttribute(input: { patch: { intValue: \""""+str(robot_info.robot_type)+"""\" }, id: \""""+str(self.ID_Dict["RobotTypeCode"])+"""\" }) {
                attribute {
                 intValue
                 }
              }
            }"""
        
        #print(smp_query)
        self.perform_graphql_request(smp_query)
        smp_query = """ 
            mutation MyMutation4 {
              updateAttribute(input: { patch: { intValue: \""""+str(robot_info.robot_capabilities)+"""\" }, id: \""""+str(self.ID_Dict["RobotCapabilities"])+"""\" }) {
                attribute {
                 intValue
                 }
              }
            }"""
        self.perform_graphql_request(smp_query)
        smp_query = """ 
            mutation MyMutation4 {
              updateAttribute(input: { patch: { stringValue: \""""+str(device_info.device.name)+"""\" }, id: \""""+str(self.ID_Dict["DeviceIdentifier"])+"""\" }) {
                attribute {
                 stringValue
                 }
              }
            }"""
        self.perform_graphql_request(smp_query)
        smp_query = """ 
            mutation MyMutation4 {
              updateAttribute(input: { patch: { stringValue: \""""+str(device_info.manufacturer.name)+"""\" }, id: \""""+str(self.ID_Dict["DeviceManufacturer"])+"""\" }) {
                attribute {
                 stringValue
                 }
              }
            }"""
        self.perform_graphql_request(smp_query)
        
        
    def send_time_series_mutation(self,ID_number,data,timesta):
        
        smp_query = """ 
            mutation MyTimeSeriesMutation {
              replaceTimeSeriesRange(
                input: {
                  attributeOrTagId: \""""+str(ID_number)+"""\"
                  entries: [
                    {
                      timestamp: \""""+timesta+"""\"
                      value: \""""+data+"""\"
                      status: "1"
                    }
                  ]
                }
              ) {
                clientMutationId

                json
              }
            }"""

        self.perform_graphql_request(smp_query)
    
    def send_time_series_struct(self,ID_number,data,timesta):
        
        starting_string="["
        for i in range(len(data)):
            starting_string+=convert_array_to_string(data[i])
            starting_string+=","
        output_string=starting_string[:-1]
        output_string+="]"
        
        smp_query = """ 
            mutation MyTimeSeriesMutation {
              replaceTimeSeriesRange(
                input: {
                  attributeOrTagId: \""""+str(ID_number)+"""\"
                  entries: [
                    {
                      timestamp: \""""+timesta+"""\"
                      value: \""""+output_string+"""\"
                      status: "1"
                    }
                  ]
                }
              ) {
                clientMutationId

                json
              }
            }"""

        self.perform_graphql_request(smp_query)
    
    
    def send_robot_state_update(self,robot_state,joint_command,vel_command):
        # attrib_command.set_value(robot.command_mode)
        # attrib_operation.set_value(robot.operational_mode)
        # attrib_con_state.set_value(robot.controller_state)
        #attrib_seqno.set_value(robot_state.seqno)
        # attrib_rob_state.set_value(robot_state.robot_state_flags)
        # attrib_joint.set_value(robot_state.joint_position)
        # attrib_effort.set_value(robot_state.joint_effort)
        # attrib_velocity.set_value(robot_state.joint_velocity)
        # #attrib_tcp.set_value(robot_state.kin_chain_tcp)
        # #attrib_tcp_vel.set_value(robot_state.kin_chain_tcp_vel
        # attrib_traj_run.set_value(robot_state.trajectory_running)
        #attrib_joint_command.set_value(joint_command)
        # attrib_joint_velocity.set_value(vel_command)
        now=datetime.now()
        timesta=now.strftime("%Y-%m-%dT%H:%M:%SZ")
        #startTime=now.strftime("%Y-%m-%d")
        #EndTime=now.strftime("%Y-%m-05")
        self.send_time_series_mutation(self.ID_Dict["CommandMode"],str(self.robot.command_mode),timesta)
        self.send_time_series_mutation(self.ID_Dict["OperationalMode"],str(self.robot.operational_mode),timesta)
        self.send_time_series_mutation(self.ID_Dict["ControllerState"],str(self.robot.controller_state),timesta)
        self.send_time_series_mutation(self.ID_Dict["seqno"],str(robot_state.seqno),timesta)
        self.send_time_series_mutation(self.ID_Dict["RobotStateFlag"],str(robot_state.robot_state_flags),timesta)
        joint_pose_string=self.convert_array_to_string(robot_state.joint_position)
        self.send_time_series_mutation(self.ID_Dict["JointPositions"],str(joint_pose_string),timesta)
        joint_effort_string=self.convert_array_to_string(robot_state.joint_effort)
        self.send_time_series_mutation(self.ID_Dict["JointEffort"],str(joint_effort_string),timesta)
        joint_velocity_string=self.convert_array_to_string(robot_state.joint_velocity)
        self.send_time_series_mutation(self.ID_Dict["JointVelocity"],str(joint_velocity_string),timesta)
        
        orientation_data=[robot_state.kin_chain_tcp.orientation.w,robot_state.kin_chain_tcp.orientation.x,robot_state.kin_chain_tcp.orientation.y,robot_state.kin_chain_tcp.orientation.z]
        position_data=[robot_state.kin_chain_tcp.position.x,robot_state.kin_chain_tcp.position.y,robot_state.kin_chain_tcp.position.z]
        self.send_time_series_struct(self.ID_Dict["KinChainTCP"],[orientation_data,position_data],timesta)
        angular_data=[robot_state.kin_chain_tcp_vel.angular.x,robot_state.kin_chain_tcp_vel.angular.y,robot_state.kin_chain_tcp_vel.angular.z]
        linear_data=[robot_state.kin_chain_tcp_vel.linear.x,robot_state.kin_chain_tcp_vel.linear.y,robot_state.kin_chain_tcp_vel.linear.z]
        self.send_time_series_struct(self.ID_Dict["KinChainTCPVel"],[angular_data,linear_data],timesta)
        
        self.send_time_series_mutation(self.ID_Dict["IsRunning"],str(robot_state.trajectory_running),timesta)
        joint_position_command=self.convert_array_to_string(joint_command)
        self.send_time_series_mutation(self.ID_Dict["JointPositionCommand"],str(joint_position_command),timesta)
        joint_velocity_command=self.convert_array_to_string(vel_command)
        self.send_time_series_mutation(self.ID_Dict["JointVelocityCommand"],str(joint_velocity_command),timesta)
    
    def perform_graphql_request(self,content):
        headers={"Authorization": self.current_bearer_token}
        url=self.args.url
        try:
            r = requests.post(url, headers=headers, data={"query": content})
            r.raise_for_status()
            print(r.json())
            return r.json()
        except requests.exceptions.HTTPError as e:
            self.requesting_new_token(e)
        #TODO Handle Errors!

    ''' Gets a JWT Token containing the Bearer string returned from the Platform, assuming authorization is granted.
        Accepts: The JSON payload you want to send to GraphQL
        Returns: The JSON payload returned from the Server '''
    def get_bearer_token (self):
        auth=self.args.authenticator
        password=self.args.password
        name=self.args.name
        url=self.args.url
        role=self.args.role
        response = self.perform_graphql_request(f"""
        mutation authRequest {{
          authenticationRequest(
            input: {{authenticator: "{auth}", role: "{role}", userName: "{name}"}}
          ) {{
            jwtRequest {{
              challenge, message
            }}
          }}
        }}
        """) 
        jwt_request = response['data']['authenticationRequest']['jwtRequest']
        if jwt_request['challenge'] is None:
            raise requests.exceptions.HTTPError(jwt_request['message'])
        else:
            print("Challenge received: " + jwt_request['challenge'])
            response=perform_graphql_request(f"""
            mutation authValidation {{
              authenticationValidation(
                input: {{authenticator: "{auth}", signedChallenge: "{jwt_request["challenge"]}|{password}"}}
                ) {{
                jwtClaim
              }}
            }}
            """)
        jwt_claim = response['data']['authenticationValidation']['jwtClaim']
        return f"Bearer {jwt_claim}"
        #TODO Handle Errors!
      
    def requesting_new_token(self,e):
        if "forbidden" in str(e).lower() or "unauthorized" in str(e).lower():
            print("Bearer Token expired!")
            print("Attempting to retreive a new GraphQL Bearer Token...")
            print()

            #Authenticate
            self.current_bearer_token = self.get_bearer_token()

            print("New Token received: " + self.current_bearer_token)
            print()

            #Re-try our data request, using the updated bearer token
            # TODO: This is a short-cut -- if this subsequent request fails, we'll crash. You should do a better job :-)
            smp_response = self.perform_graphql_request(smp_query, headers={"Authorization": self.current_bearer_token})
        else:
            print("An error occured accessing the SM Platform!")
            print(e)
            exit(-1)

def main():
    instance_graphql_endpoint = "https://interfacetech.cesmii.thinkiq.net/graphql"
    sample_rate=2
    ''' You could opt to manually update the bearer token that you retreive from the Developer menu > GraphQL - Request Header token
          But be aware this is short-lived (you set the expiry, see Authenticator comments below) and you will need to handle
          expiry and renewal -- as shown below. As an alternative, you could start your life-cycle with authentication, or
          you could authenticate with each request (assuming bandwidth and latency aren't factors in your use-case). '''
    current_bearer_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiaW50ZXJmYWNldGVjaF9ncm91cCIsImV4cCI6MTY0Njg0MDA5NiwidXNlcl9uYW1lIjoiaW50ZXJmYWNldGVjaDI3IiwiYXV0aGVudGljYXRvciI6ImludGVyZmFjZXRlY2giLCJhdXRoZW50aWNhdGlvbl9pZCI6IjI5IiwiaWF0IjoxNjQ2ODM4Mjk2LCJhdWQiOiJwb3N0Z3JhcGhpbGUiLCJpc3MiOiJwb3N0Z3JhcGhpbGUifQ.4-bK6jJJmrCaQKf-ztOd1hCLprMg-4D_SBzSsEKBIhY"
    # eg: Bearer eyJyb2xlIjoieW91cl9yb2xlIiwiZXhwIjoxNDk5OTk5OTk5LCJ1c2VyX25hbWUiOiJ5b3VydXNlcm5hbWUiLCJhdXRoZW50aWNhdG9yIjoieW91cmF1dGgiLCJhdXRoZW50aWNhdGlvbl9pZCI6Ijk5IiwiaWF0Ijo5OTk5OTk5OTk5LCJhdWQiOiJhdWQiLCJpc3MiOiJpc3MifQ==
    
    parser = argparse.ArgumentParser()
    ''' These values come from your Authenticator, which you configure in the Developer menu > GraphQL Authenticator
        Rather than binding this connectivity directly to a user, we bind it to an Authenticator, which has its own
        credentials. The Authenticator, in turn, is linked to a user -- sort of like a Service Principle.
        In the Authenticator setup, you will also configure role, and Token expiry. '''
    parser.add_argument("-a", "--authenticator", type=str, default="RobotDataSend", help="Authenticator Name")
    parser.add_argument("-p", "--password", type=str, default="Freedom5!!", help="Authenticator Password")
    parser.add_argument("-n", "--name", type=str, default="interfacetech27", help="Authenticator Bound User Name")
    parser.add_argument("-r", "--role", type=str, default="interfacetech_group", help="Authenticator Role")
    parser.add_argument("-u", "--url", type=str, default=instance_graphql_endpoint, help="GraphQL URL")
    args = parser.parse_args()
    graphql_sender=GraphQL_sender(args,current_bearer_token)
    #graphql_sender.convert_array_to_string([3.0,55.0,6.0])

    RRC.RegisterStdRobDefServiceTypes(RRN)
    robosewclient='192.168.51.61'
    #url='rr+tcp://'+robosewclient+':58651?service=robot'://[fe80::b852:412a:6117:baa0]:11111/?
    url='rr+tcp://[fe80::b852:412a:6117:baa0]:11111/?service=robot'
    robot_sub=RRN.SubscribeService(url)
    robot_sub.ClientConnectFailed += connect_failed
    state_w = robot_sub.SubscribeWire("robot_state")
    cmd_w = robot_sub.SubscribeWire('position_command')
    vel_w = robot_sub.SubscribeWire("velocity_command")
    time.sleep(1)
    robot=robot_sub.GetDefaultClientWait(1)
    robot_device_info=robot.device_info
    robot_info=robot.robot_info
    graphql_sender.assign_RR_robot(robot)
    graphql_sender.send_initial_robot_data(robot_info,robot_device_info)
    
    while True:
        robot_state=state_w.InValue
        joint_command=cmd_w.InValue.command
        vel_command=vel_w.InValue.command
        graphql_sender.send_robot_state_update(robot_state,joint_command,vel_command)
        time.sleep(sample_rate)

if __name__ == "__main__":
    main()
    # #server_url = "opc.tcp://opcua.interfacetech.cesmii.net:51210" opc.tcp://localhost:62548/Quickstarts/DataAccessServer
    # server_url = "opc.tcp://localhost:62548/"
    # server_name = "ROBOT_SERVER"
    # sample_rate = 2

    # print("Configuring Simple OPC UA Server...")
    # my_ua_server = Server()
    # my_ua_server.set_endpoint(server_url)

    # # Register a new namespace to work in
    # my_ua_namespace = my_ua_server.register_namespace(server_name)
    # print("Namespace ID: {}".format(my_ua_namespace))

    # # Find the "Objects" folder to attach a new object to
    # my_ua_node = my_ua_server.get_objects_node()
    # print("Objects Node ID: ", my_ua_node)

    # # Create a new object
    # my_object = my_ua_node.add_object(my_ua_namespace, "Robot 1")
    # print("MyObject ID:", my_object)

    # # Add some attributes (of type variable) to MyObject
    # attrib_command = my_object.add_variable(my_ua_namespace, "Command Mode", 0)
    # attrib_operation = my_object.add_variable(my_ua_namespace, "Operational Mode", 0)
    # attrib_con_state = my_object.add_variable(my_ua_namespace, "Controller State", 0)
    # attrib_joint = my_object.add_variable(my_ua_namespace, "Joint Positions", 0.0)
    # attrib_effort = my_object.add_variable(my_ua_namespace, "Joint Effort", 0.0)
    # attrib_velocity = my_object.add_variable(my_ua_namespace, "Joint Velocity", 0.0)
    # attrib_tcp = my_object.add_variable(my_ua_namespace, "Kin chain TCP", 0.0)
    # attrib_tcp_vel = my_object.add_variable(my_ua_namespace, "Kin Chain TCP vel", 0.0)
    # attrib_rob_state = my_object.add_variable(my_ua_namespace, "Robot State Flag", 0)
    # attrib_seqno = my_object.add_variable(my_ua_namespace, "seqno", 0)
    # attrib_joint_command = my_object.add_variable(my_ua_namespace, "Joint Position Command", 0.0)
    # attrib_joint_velocity = my_object.add_variable(my_ua_namespace, "Joint Velocity Command", 0.0)
    # attrib_error = my_object.add_variable(my_ua_namespace, "Current Error", "System Started but Robot Raconteur Connection Not Found")
    # attrib_traj_run = my_object.add_variable(my_ua_namespace, "Trajectory Running", False)


    # attrib_type = my_object.add_variable(my_ua_namespace, "Robot Type Code", 0)
    # attrib_capabilities = my_object.add_variable(my_ua_namespace, "Robot Capabilities", 0)
    # attrib_device = my_object.add_variable(my_ua_namespace, "Device Identifier", 0)
    # attrib_manufacturer = my_object.add_variable(my_ua_namespace, "Device Manufacturer", "Device Manufacturer")

    # # This attribute value can be written to by a client
    # #attrib_toggler = my_object.add_variable(my_ua_namespace, "Toggle Bit", False)
    # #attrib_toggler.set_writable()
    # RRC.RegisterStdRobDefServiceTypes(RRN)
    # robosewclient='192.168.51.61'
    # url='rr+tcp://'+robosewclient+':58651?service=robot'
    # try:
        # my_ua_server.start()
        # while True:
            # attrib_command.set_value(15)
            # time.sleep(sample_rate)
    # except KeyboardInterrupt:
        # print("Press Ctrl-C to terminate while statement")
        # my_ua_server.stop()
    # pass
    # robot_sub=RRN.SubscribeService(url)
    # robot_sub.ClientConnectFailed += connect_failed
    # state_w = robot_sub.SubscribeWire("robot_state")
    # cmd_w = robot_sub.SubscribeWire('position_command')
    # vel_w = robot_sub.SubscribeWire("velocity_command")

    # robot=robot_sub.GetDefaultClientWait(1)

    # #robot_const = RRN.GetConstants("com.robotraconteur.robotics.robot", robot)
    
    # # state_w.WireValueChanged+=robot_state_update
    # # cmd_w.WireValueChanged+=robot_command_update
    # # vel_w.WireValueChanged+=robot_vel_update
    


    # try:
        # print()
        # print("Starting Simple OPC UA Server...")
        # my_ua_server.start()
        # print()
        # print("Generating Sample Data...")
        # robot_device_info=robot.device_info
        # robot_info=robot.robot_info
        # attrib_type.set_value(robot_info.robot_type)
        # attrib_capabilities.set_value(robot_info.robot_capabilities)
        # attrib_device.set_value(robot_device_info.device.name)
        # attrib_manufacturer.set_value(robot_device_info.manufacturer.name)
        
        

        # while True:
            # #Update the attribute values for my object
            # attrib_command.set_value(robot.command_mode)
            # attrib_operation.set_value(robot.operational_mode)
            # attrib_con_state.set_value(robot.controller_state)
            
            # #####attrib_error
            
            # robot_state=state_w.InValue
            # attrib_seqno.set_value(robot_state.seqno)
            # attrib_rob_state.set_value(robot_state.robot_state_flags)
            # attrib_joint.set_value(robot_state.joint_position)
            # attrib_effort.set_value(robot_state.joint_effort)
            # attrib_velocity.set_value(robot_state.joint_velocity)
            # #attrib_tcp.set_value(robot_state.kin_chain_tcp)
            # #attrib_tcp_vel.set_value(robot_state.kin_chain_tcp_vel
            # attrib_traj_run.set_value(robot_state.trajectory_running)
            
            
            
            # joint_command=cmd_w.InValue.command
            # attrib_joint_command.set_value(joint_command)
            
            # vel_command=vel_w.InValue.command
            # attrib_joint_velocity.set_value(vel_command)
            # #attrib_joint.set_value(joints)
            # #attrib_press.set_value(computer.virtual_memory.used_percent)

            # print ("Current values: ", attrib_joint.get_value())

            # time.sleep(sample_rate)
    # finally:
        # my_ua_server.stop()
        # print("Server Offline")

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
    
