import json

from flask import Flask, render_template

app = Flask(__name__)

template_blog_posts = [
    {"id": 1, "author": "John Doe", "title": "First Post", "content": "This is my first post."},
    {"id": 2, "author": "Jane Doe", "title": "Second Post", "content": "This is another post."}
    # More blog posts can go here...
]


@app.route('/')
def index():
    """
    Base route for all blog posts to be presented.
    """
    # add code here to fetch the blog posts from a file
    with open('db.json', 'r', encoding='utf-8') as db_file:
        blog_posts = json.load(db_file)
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)