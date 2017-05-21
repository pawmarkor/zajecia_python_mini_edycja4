import argparse

from pathlib import Path

from dir_explorer.utils import (
    delete_tree,
    create_tree,
    print_error,
    demo_tree,
)
import dir_explorer.configuration as conf


def runserver():

    args = parse_args(
        "Run dir_explorer server",
        (("--port",), {"type": int,
                       "help": "Set port"}),
        (("--host",), {"help": "Set host"}),
        (("--debug",), {"action": "store_true",
                        "help": "Run app in debug mode"}),
    )

    if args.port is not None:
        conf.port = args.port
    if args.host is not None:
        conf.host = args.host
    conf.debug = args.debug

    from dir_explorer.application import app
    app.run(port=conf.port, host=conf.host, debug=conf.debug)


def remove_demo_data():
    parse_args("Remove demo data")
    try:
        delete_tree(conf.explore_dir)
    except OSError as error:
        print_error("Unable to remove demo data because of {}".format(error))
        exit(1)
    else:
        print("Demo data removed")


def create_demo_data():
    parse_args("Create demo data")
    try:
        create_tree(demo_tree, conf.explore_dir.parent)
    except OSError as error:
        print_error("Unable to create demo data because of {}".format(error))
        exit(1)
    else:
        print("Demo data created")


def parse_args(description, *arguments):
    parser = argparse.ArgumentParser(
        description=description
    )
    parser.add_argument("--explore_dir", help="Set base dir for exploration")
    for argument in arguments:
        parser.add_argument(*argument[0], **argument[1])

    args = parser.parse_args()

    for name, value in vars(args).items():
        if value is not None:
            setattr(conf, name, value)

    conf.explore_dir = Path(conf.explore_dir)

    return args
