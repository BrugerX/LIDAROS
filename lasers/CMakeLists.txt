cmake_minimum_required(VERSION 3.5)
project(lasers)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)

# 1. Generate the message
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/setlaserpower.srv"
  DEPENDENCIES std_msgs
)

# 2. If you have Python nodes in the same package:
ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  src/lasernode.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
