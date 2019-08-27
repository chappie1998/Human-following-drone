# Human-following-drone

## Description:- 
  As drones become more and more complex, there are many different features that users can pick from. Having a drone camera that follows you has a unique appeal for those in the filming and videography realm: the pilot can lock the 'drone's direction on a very specified moving target.
  
  After the pilot selects this function, the drone will then follow the target without needing to use the 'pilot's input for control, by use of sensors, and software that allows the device to lock in on specific objects. While this feature is activated, the individual flying can focus on their own choice of creative photo and video elements, not having to worry about the duties of stabilizing flight.
  
  Some of the other benefits of a self-following drone are for more comfortable filming of action sports: a subject such as a mountain biker or skateboarder can be followed with this feature, and having the perspective from overhead will add to the richness of the clip. When a drone follows you from overhead, everything from jumps you are taking, marathon steps you are running through, or obstacles you are grinding on or flying over with a skateboard will come to life.

  I present you my project "The human following drone." It is based on image processing(Open CV) algorithm with ROS(robot operating system).


## Hardware requirement:-

1. A drone kit
2. A Pixhawk full kit
3. Raspberry Pi
4. Raspberry pi camera
5. Power bank
6. WIFI router(video transmit)
7. A laptop

## Prerequisites:-

1. ROS(robot operating system)
2. Open CV(Image processing)
3. Mavros(drone package)
4. dlib(library)
5. socket(library)
6. Picamera(library for raspberry pi)

## Workspace setup:-
   Mavros package is being used in this project. This package is a ROS package which provides communication driver for various autopilots with MAVLink communication protocol. Additional it provides UDP MAVLink bridge for ground control stations (e.g., QGroundControl).
   
If you want to know more about mavros package follow this link:- http://wiki.ros.org/mavros

  For setup mavros and Gazebo workspace(drone simulation), all instruction are in [ROS and Gazebo Installation.odt](https://github.com/ankitgc1/Human-following-drone/blob/master/setup/ROS%20and%20Gazebo%20Installation.odt) file. Follow the given instruction.
  
Example code is taken from here, and the setup process has taken from here.(just for reference)
After all the process, If everything went right, You should now see the drone takeoff in the simulator.


### Simulation:- 
  The simulation is useful for every project. So, let's try the simulation. There are two files one uses your system webcam's stream, and the other one uses the raspberry pi stream(for this step2, and step3 should be completed). Run drone_publisher_webcam.py script for your system's webcam and then drone_subscribe.py script. 

## Project setup:-
### Step 1:-
The PX4 software used in the project. PX4 is an open-source flight control software for drones and other unmanned vehicles. For assembling the drone and and configuration follow this [tutorial.](https://docs.px4.io/master/en/assembly/) 

to know more about PX4:- https://px4.io/

##### Checking:- 
Check the position hold mode. This mode should work fine for this project. 

### Step 2:- 
  Install ubuntu mate 18.04 OS in the raspberry pi. It is easy to install and use the ROS in ubuntu. After that install ROS in raspberry pi. Clone raspberry pi's code in the raspberry pi. You also need ROS in surface computer. Make same ROS master for both systems. 

##### Checking:- 
Run ROS master on the surface computer and get a list of topics on raspberry pi.

### Step 3:- 
  Attach the raspberry pi and pi cam to the drone. Through USB cable connect raspberry pi and pixhawk. Connect the raspberry pi and the surface computer on the same the network(for now mobile hotspot can be used). #Check surface computer's IP address and put it in raspberry pi's and surface computer's code.

##### Checking:- 
Run the surface computer's stream_server_test.py script on the surface computer and then run stream_fast.py script on raspberry pi. Now the video stream of your raspberry pi should be able to stream on your surface computer.

#### Note:- Always run surface computer's streaming code first, after running this code you should run the raspberry pi's code. Otherwise, you will get an error in raspberry pi's code.

### Step 4:- 
  The setup is all most done. For safety, recheck all things. Run drone_publisher.py script on the surface computer, Now run stream_fast.py script on raspberry pi. Finally, run drone_subscriber.py script on the surface computer.

Go and play around your drone. 

