from app import create_app, db
from app.models import User, BlogPost, Comment

app = create_app()


def create_dummy_data():

    with app.app_context():
        # Create a dummy user
        user = User(username='dummy_user', email='dummy@example.com')
        user.set_password('password123')  # Assuming you have a method to hash passwords
        db.session.add(user)
        db.session.commit()

        # Create a dummy blog post
        post = BlogPost(title='Hello World', content='This is a test blog post.', user_id=user.id)
        db.session.add(post)
        db.session.commit()

        # Create some dummy comments
        comment1 = Comment(content='First comment on the post.', user_id=user.id, post_id=post.id)
        db.session.add(comment1)

        comment2 = Comment(content='Reply to the first comment.', user_id=user.id, post_id=post.id, parent_id=comment1.id)
        db.session.add(comment2)

        db.session.commit()
    
if __name__ == '__main__':
    create_dummy_data()
    print('Dummy data created.')