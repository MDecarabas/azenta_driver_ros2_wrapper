from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()
    peeler_controller = Node(
        package="peeler_controller",
        executable="peeler_controller",
        output='screen',
        parameters=[{"name": "peeler"}],
        emulate_tty=True,
        arguments=['--ros-args', '--log-level', 'INFO']
    )
    ld.add_action(peeler_controller)
    return ld
