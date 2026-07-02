import json

from flask import Flask, url_for, request, render_template, redirect

app = Flask(__name__)

template_blog_posts = [
    {"id": 1, "author": "John Doe", "title": "First Post", "content": "This is my first post."},
    {"id": 2, "author": "Jane Doe", "title": "Second Post", "content": "This is another post."}
    # More blog posts can go here...
]

def get_db() -> dict:
    """
    Opens the db.JSON file and returns all entries as a dict.
    :return db_file: dict with all entries.
    """
    with open('db.json', 'r', encoding='utf-8') as db_file:
        return json.load(db_file)

def get_next_id() -> int:
    """
    Gets the next uninstantiated id from the db.JSON file and returns it.
    :return next_id: next uninstantiated id from the db.JSON file:
    """
    json_db = get_db()
    return json_db['next_id']

def db_fetch_all():
    """
    Simulates a SELECT * FROM db.JSON file and returns all entries as a dict.
    :return:
    """
    json_db = get_db()
    return json_db['data']

def db_commit(json_db: dict) -> None:
    """
    Simulates a COMMIT the db.JSON file.
    :param json_db: The JSON / dictionary construct to be saved into the db.JSON file:
    """
    with open('db.json', 'w', encoding='utf-8') as db_file:
        db_file.write(json.dumps(json_db))

def insert_into(blog_post: dict) -> None:
    """
    Simulates a INSERT into db.JSON file.
    :param blog_post:
    :return None:
    """
    json_db  = get_db()
    json_db['data'].append(blog_post)
    json_db['next_id'] += 1
    db_commit(json_db)
    print(f'Blog post {blog_post['title']} saved to db.')
    return None

def delete_from(blogpost_id: int) -> None:
    """
    Simulates a DELETE from db.JSON file.
    :param blogpost_id: The id of the blog post to be deleted.
    """
    json_db = get_db()
    new_rows = []
    for row in json_db['data']:
        if row['id'] != blogpost_id:
            new_rows.append(row)
    json_db['data'] = new_rows
    db_commit(json_db)
    print(f'Blog post {blogpost_id} deleted from db.')
    return None

@app.route('/')
def index():
    """
    Base route for all blog posts to be presented.
    """
    # add code here to fetch the blog posts from a file
    blog_posts = db_fetch_all()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Route for adding a new blog post.
    On 'GET' the form will be served, a new entry will be added otherwise.
    """
    if request.method == 'POST':
        new_post = {'id': get_next_id(),
                    'author': request.form['author'],
                    'title': request.form['title'],
                    'content': request.form['content'],}
        insert_into(new_post)
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    Route for deleting a blog post.
    :param post_id: The id of the blog post to be deleted.
    """
    delete_from(post_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)