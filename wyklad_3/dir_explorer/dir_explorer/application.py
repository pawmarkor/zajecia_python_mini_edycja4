from pathlib import Path
from werkzeug.routing import PathConverter
from flask import Flask, render_template, redirect, url_for, abort

from dir_explorer.file_walker import my_dir_walker_with_size_counting
from dir_explorer.configuration import explore_dir

tree_data = my_dir_walker_with_size_counting(
    explore_dir,
    topname=explore_dir.name
)


class PathLibPathConverter(PathConverter):
    def to_python(self, path):
        return Path(path)


app = Flask(__name__)
app.url_map.converters['Path'] = PathLibPathConverter


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        'not_found.html',
        root_path=explore_dir.name,
    )


@app.route('/stats/', methods=['GET'])
@app.route('/stats/<Path:path>', methods=['GET'])
def stats(path=None):
    if path is None:
        return redirect(url_for('stats', path=explore_dir.name))
    curr_tree = tree_data
    path_parts = path.parts
    for path_part in path_parts:
        try:
            curr_tree = curr_tree.children[path_part]
        except KeyError:
            if len(path_parts) == 1 and path_parts[0] == explore_dir.name:
                app.logger.error(
                    'The explore dir {} does not exist'.format(str(explore_dir))
                )
                abort(500)
            abort(404)
    parent_path = path.parent

    return render_template(
        'stats.html',
        tree_data=curr_tree,
        parent_path=parent_path if parent_path != Path('.') else None,
        path=path,
    )
