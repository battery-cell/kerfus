cmake_minimum_required(VERSION 3.8)
project(kerfus_sim)

find_package(ament_cmake REQUIRED)

# cad/ and docs/ are for you and are not installed.
install(DIRECTORY urdf worlds config launch meshes maps rviz
  DESTINATION share/${PROJECT_NAME})

ament_package()
