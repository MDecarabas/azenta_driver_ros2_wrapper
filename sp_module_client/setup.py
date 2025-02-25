from setuptools import setup

package_name = 'sp_module_client'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='decarabas',
    maintainer_email='rpl@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'peelerNode = sp_module_client.peelerNode:main',
            'sealerNode = sp_module_client.sealerNode:main',
            'cameraNode = sp_module_client.cameraNode:main',
            'masterNode = sp_module_client.masterNode:main',
        ],
    },
)

