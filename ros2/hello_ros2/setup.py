from setuptools import setup

package_name = 'hello_ros2'

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
    maintainer='suhas',
    maintainer_email='suhas.g96.sg@gmail.com',
    description='Publisher/Subscriber demo for JDERobots GSOC 2021 challenge using rclpy',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = hello_ros2.publisher_member_function:main',
            'listener = hello_ros2.subscriber_member_function:main',
        ],
    },
)
