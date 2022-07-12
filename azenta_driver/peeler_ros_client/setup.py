import os
from setuptools import find_packages, setup



install_requires = []
with open('requirements.txt') as reqs:
    for line in reqs.readlines():
        req = line.strip()
        if not req or req.startswith('#'):
            continue
        install_requires.append(req)


package_name = "peeler_ros_client"

setup(
    name = package_name,
    version="0.0.1",
    packages=find_packages(),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=install_requires,
    zip_safe=True,
    maintainer="Doga Ozgulbas",
    maintainer_email="dozgulbas@anl.gov",
    description="ROS Node for Peeler ros client",
    url='', 
    license="MIT License",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [

        ],
    },
)
