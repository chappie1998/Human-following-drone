cmake_minimum_required(VERSION 2.8.3)
project(takeoff)

## Find catkin and any catkin packages
find_package(catkin REQUIRED COMPONENTS roscpp geometry_msgs mavros_msgs)

## Declare a catkin package
catkin_package()

## Build talker and listener
include_directories(include ${catkin_INCLUDE_DIRS})

add_executable(offb_node src/offb_node.cpp)
target_link_libraries(offb_node ${catkin_LIBRARIES})
