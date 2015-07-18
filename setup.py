from setuptools import setup

setup(
    name="PyBCI",
    version="0.0.1",
    description="Streams OpenBCI data via stdio and websockets",
    url='http://github.com/hynek/pem/',
    license='MIT',
    author='Nat Noordanus',
    author_email='n@natn.me',
    include_package_data=True,
    py_modules=['pybci','lib']
    install_requires=[
        "tornado",
        "serial",
        "numpy"
    ]
)
