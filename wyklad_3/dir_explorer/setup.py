from setuptools import find_packages, setup

project = "dir_explorer"
version = "0.0.1"

setup(
    name=project,
    version=version,
    description="Dir Explorer",
    author="Paweł Kordowski",
    author_email="paw.mar.kor@gmail.com",
    url="https://github.com/pawmarkor/zajecia_python_mini_edycja4"
        "/tree/master/wyklad_3/dir_explorer",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords='dir_explorer',
    install_requires=[
        "flask==0.12.2",
    ],
    entry_points={
        "console_scripts": [
            "create_demo_data = dir_explorer.main:create_demo_data",
            "remove_demo_data = dir_explorer.main:remove_demo_data",
            "runserver = dir_explorer.main:runserver",
        ]
    },
)
