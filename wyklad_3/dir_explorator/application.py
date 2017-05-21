from pathlib import Path
from werkzeug.routing import PathConverter
from file_walker import my_dir_walker_with_size_counting
from flask import Flask, render_template, redirect, url_for, abort

root_dir = Path(
    '/home/pawkor/zajecia_python_mini_edycja4/wyklad_3/dir_explorator',
)
test_dir = Path('test dir')
full_test_path = root_dir / test_dir

tree_data = my_dir_walker_with_size_counting(full_test_path, topname=test_dir)


class PathLibPathConverter(PathConverter):
    def to_python(self, path):
        return Path(path)


app = Flask(__name__)
app.url_map.converters['Path'] = PathLibPathConverter


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        'not_found.html',
        root_path=test_dir,
    )


@app.route('/stats/', methods=['GET'])
@app.route('/stats/<Path:path>', methods=['GET'])
def stats(path=None):
    if path is None:
        return redirect(url_for('stats', path=test_dir))
    curr_tree = tree_data
    for path_part in path.parts:
        try:
            curr_tree = curr_tree.children[path_part]
        except KeyError:
            abort(404)
    parent_path = path.parent

    return render_template(
        'stats.html',
        tree_data=curr_tree,
        parent_path=parent_path if parent_path != Path('.') else None,
        path=path,
    )


if __name__ == "__main__":
    app.run()
