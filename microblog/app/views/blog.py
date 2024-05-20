from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import BlogPost, Comment

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/', methods=['GET'])
def index():
    return jsonify({"msg": "Welcome to the blogging API"}), 200


@blog_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    post = BlogPost(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return jsonify({"msg": "Post created"}), 201

@blog_bp.route('/posts/<int:post_id>/comments', methods=['POST', 'GET'])
@jwt_required()
def post_comments(post_id):
    if request.method == 'POST':
        user_id = get_jwt_identity()
        data = request.get_json()
        content = data.get('content')
        parent_id = data.get('parent_id')

        comment = Comment(content=content, user_id=user_id, post_id=post_id, parent_id=parent_id)
        db.session.add(comment)
        db.session.commit()

        return jsonify({"msg": "Comment created"}), 201
    elif request.method == 'GET':
        comments = Comment.query.filter_by(post_id=post_id).all()
        comments_data = [{"id": c.id, "content": c.content, "user": c.user.username, "replies": get_replies(c)}
                         for c in comments if c.parent_id is None]

        return jsonify(comments_data), 200

def get_replies(comment):
    return [{"id": r.id, "content": r.content, "user": r.user.username} for r in comment.replies]

@blog_bp.route('/posts/<int:post_id>', methods=['GET'])
def view_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id, parent_id=None).all()

    def fetch_replies(comment):
        replies = Comment.query.filter_by(parent_id=comment.id).all()
        for reply in replies:
            reply.replies = fetch_replies(reply)
        return replies

    for comment in comments:
        comment.replies = fetch_replies(comment)

    return render_template('comment_thread.html', post=post, comments=comments)
