# dir_explorer

Simple flask based web app for exploring a given server directory and computing size of items.

## Quickstart

The project is written in Python3.5

Being in the project directory install the project via:

    pip install -e .

Create demo data via:

    create_demo_data

Run the server via:

    runserver

In order to remove the demo data use:

    remove_demo_data

In the web browser open [localhost:8000/stats](localhost:8000/stats)

## Configuration

You can specify port, host, directory to be explored and turn the debug mode while running `runserver`

    runserver --port 5000 --host my_host --explore_dir my_path --debug

The default directory to be explore is `./test dir`, it is not kept in the repository
so you either should use `create_demo_data` or create it on your own. 

You can change the explored directory using `--explore_dir` flag
while running any of `create_demo_data`, `remove_demo_data` and `runserver`.

Please note that 

    remove_demo_data -d my_path

will remove `my_path` from your OS
(i.e. not only demo files but also all the files in `my_path`) **be carefull, using it may be dangerous!**

## Testing

In order to run tests execute:

    python setup.py nosetests