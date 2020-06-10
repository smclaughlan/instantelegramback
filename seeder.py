from dotenv import load_dotenv
load_dotenv()

# Regardless of the lint error you receive,
# load_dotenv must run before running this
# so that the environment variables are
# properly loaded.
from app import app, db
from app.models import User, Follow, Post


with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User(
        username='Riki',
        hashed_password='ljalsdfj',
        email='em234ail@email.com',
        bio='bio good',
    )
    user2 = User(
        username='Riki2',
        hashed_password='lja2fflsdfj',
        email='ema243il2@email.com',
        bio='bio2 good',
    )
    follow = Follow(
        follower=user1,
        followed=user2,
    )
    post1 = Post(
        image='https://res.cloudinary.com/dgzcv1mcs/image/upload/v1591737505/ma9c57wqt1dioyxd3gdc.jpg',
        caption='Ravesignal III',
        poster=user1,
    )

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(follow)
    db.session.add(post1)
    db.session.commit()
