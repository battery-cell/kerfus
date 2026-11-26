#!/usr/bin/env bash
# One-command Kerfus simulation demos.
#
# Usage:
#   ./run_sim.sh                        build, then SLAM + RViz + teleop
#   ./run_sim.sh --nav                  build, then Nav2 + RViz + rqt_graph
#   ./run_sim.sh --no-build             skip colcon build
#   ./run_sim.sh world:=/path/room.sdf  use a different Gazebo world
#   ./run_sim.sh map:=/path/map.yaml    use another map with --nav
#   ./run_sim.sh teleop:=true           also open teleop in --nav mode
#   ./run_sim.sh --help                 show this help
#
# In the default demo, use the teleop terminal to drive and watch the SLAM map
# grow in RViz. In --nav mode, use the Nav2 Goal tool in RViz to navigate on
# maps/room.yaml and inspect the ROS graph in rqt_graph. Ctrl-C stops everything.
set -eo pipefail

HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
WS="$HERE/ros2_ws"
DISTRO="${ROS_DISTRO:-humble}"
ROS_SETUP="${ROS_SETUP:-/opt/ros/$DISTRO/setup.bash}"

usage() {
    sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'
}

BUILD=1
LAUNCH_FILE=bringup.launch.py
NO_TELEOP=0
NO_RVIZ=0
NO_SLAM=0
LAUNCH_ARGS=()
for arg in "$@"; do
    case "$arg" in
        --nav)        LAUNCH_FILE=nav_demo.launch.py ;;
        --no-build)   BUILD=0 ;;
        --no-teleop)  NO_TELEOP=1 ;;
        --no-rviz)    NO_RVIZ=1 ;;
        --no-slam)    NO_SLAM=1 ;;
        -h|--help)    usage; exit 0 ;;
        *)            LAUNCH_ARGS+=("$arg") ;;
    esac
done
if ((NO_TELEOP)); then
    LAUNCH_ARGS+=('teleop:=false')
fi
if ((NO_RVIZ)); then
    LAUNCH_ARGS+=('rviz:=false')
fi
if ((NO_SLAM)) && [[ "$LAUNCH_FILE" == bringup.launch.py ]]; then
    LAUNCH_ARGS+=('slam:=false')
fi

if [[ ! -f "$ROS_SETUP" ]]; then
    echo "error: $ROS_SETUP not found. Is ROS 2 $DISTRO installed?" >&2
    exit 1
fi
if [[ ! -d "$WS/src/kerfus_sim" ]]; then
    echo "error: $WS/src/kerfus_sim not found." >&2
    exit 1
fi

# ROS setup scripts are not safe with `set -u`; this script does not enable it.
# shellcheck disable=SC1090
source "$ROS_SETUP"

missing=()
required=(ros_gz_sim ros_gz_bridge teleop_twist_keyboard rviz2)
if [[ "$LAUNCH_FILE" == bringup.launch.py ]]; then
    required+=(slam_toolbox)
fi
if [[ "$LAUNCH_FILE" == nav_demo.launch.py ]]; then
    required+=(nav2_bringup rqt_graph)
fi
for pkg in "${required[@]}"; do
    if [[ ! -d "/opt/ros/$DISTRO/share/$pkg" ]]; then
        missing+=("ros-$DISTRO-${pkg//_/-}")
    fi
done
if ! command -v ign >/dev/null 2>&1; then
    missing+=("ros-$DISTRO-ros-gz")
fi
if ((${#missing[@]} > 0)); then
    echo "error: missing packages: ${missing[*]}" >&2
    echo "Install them with:" >&2
    printf '  sudo apt update && sudo apt install %s\n' \
        "$(printf '%s\n' "${missing[@]}" | sort -u | tr '\n' ' ')" >&2
    exit 1
fi

if ((BUILD)); then
    if ! command -v colcon >/dev/null 2>&1; then
        echo "error: colcon not found (use --no-build if the workspace is built)." >&2
        exit 1
    fi

    # The checked-in build/ tree may have been produced on another machine.
    # Reconfigure from scratch if its paths do not point at this workspace.
    cmake_cache="$WS/build/kerfus_sim/CMakeCache.txt"
    clean_args=()
    if [[ -f "$cmake_cache" ]] && \
       ! grep -qF "CMAKE_HOME_DIRECTORY:INTERNAL=$WS/src/kerfus_sim" "$cmake_cache"; then
        echo "[run_sim] Stale colcon cache found; reconfiguring from scratch."
        clean_args=(--cmake-clean-cache --cmake-force-configure)
    fi

    echo "[run_sim] Building kerfus_sim..."
    (
        cd "$WS"
        colcon build --packages-select kerfus_sim --symlink-install "${clean_args[@]}"
    )
fi

if [[ ! -f "$WS/install/setup.bash" ]]; then
    echo "error: $WS/install/setup.bash not found; run without --no-build." >&2
    exit 1
fi
# shellcheck disable=SC1091
source "$WS/install/setup.bash"

if [[ "$LAUNCH_FILE" == nav_demo.launch.py ]]; then
    echo "[run_sim] Starting Gazebo + robot + Nav2 + RViz + rqt_graph."
    echo "[run_sim] Use the Nav2 Goal tool in RViz to send the robot somewhere."
else
    echo "[run_sim] Starting Gazebo + robot + SLAM + RViz."
    echo "[run_sim] Teleop keys open in a new terminal; drive around and watch /map fill in."
fi

exec ros2 launch kerfus_sim "$LAUNCH_FILE" "${LAUNCH_ARGS[@]}"
