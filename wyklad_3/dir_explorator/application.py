import os
from file_walker import my_dir_walker_with_size_counting, EntityData
from flask import Flask, render_template, redirect, url_for, abort
app = Flask(__name__)

root_dir = '/home/pawkor/zajecia_python_mini_edycja4/wyklad_3/dir_explorator'
test_dir = 'test dir'
full_test_path = os.path.join(root_dir, test_dir)

tree_data = my_dir_walker_with_size_counting(full_test_path)[full_test_path]
tree_data = EntityData('', '', {test_dir: tree_data})


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        'not_found.html',
        root_path=test_dir,
    )


@app.route('/stats/', methods=['GET'])
@app.route('/stats/<path:path>', methods=['GET'])
def stats(path=None):
    if path is None:
        return redirect(url_for('stats', path=test_dir))
    curr_tree = tree_data
    path_parts = []
    head = path
    while head:
        head, tail = os.path.split(head)
        if tail:
            path_parts.append(tail)
    for path_part in reversed(path_parts):
        try:
            curr_tree = curr_tree.children[path_part]
        except KeyError:
            abort(404)
    parent_path = os.path.join(*os.path.split(path)[:-1])

    return render_template(
        'stats.html',
        tree_data=curr_tree,
        parent_path=parent_path,
        path=path,
    )

if __name__ == "__main__":
    app.run()