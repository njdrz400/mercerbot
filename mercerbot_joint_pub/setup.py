from setuptools import setup

package_name = 'mercerbot_joint_pub'

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
    maintainer='SMIZEREK',
    maintainer_email='mizereks@mccc.edu',
    description='Joint state GUI publisher',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # command name  = python_module:function
            'joint_slider_gui = mercerbot_joint_pub.joint_slider_gui:main',
        ],
    },
)
