# rosidl_opendds_adapter

OpenDDS .idl file generator from ROS2 .msg, .srv files.
This package is based on rosidl_adapter.

Tested on ROS2 Humble.

## Getting Started

### Installing & Building

Clone this package into your ROS2 workspace. And build it.

```
cd /your/ros2/workspace/src
git clone https://github.com/NTques/rosidl_opendds_adapter.git

cd ..
colcon build --packages-select rosidl_opendds_adapter

source install/setup.bash
```

### Command

Compile a .msg file. .idl file located on /path/to/msg/file/path

```
ros2 run rosidl_opendds_adapter msg2idl.py /path/to/msg/file/path
```

Compile .msg files. .idl file located on /path/to/msg/file/dir

```
ros2 run rosidl_opendds_adapter msg2idl.py /path/to/msg/files/dir/*.msg
```

Compile a .srv file. .idl file located on /path/to/srv/file/path

```
ros2 run rosidl_opendds_adapter srv2idl.py /path/to/srv/file/path
```

Compile .srv files. .idl file located on /path/to/srv/file/dir

```
ros2 run rosidl_opendds_adapter srv2idl.py /path/to/srv/files/dir/*.srv
```
