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
        hashed_password='pbkdf2:sha256:150000$ltOXv3W8$6e1e42bfc60f89dde0a8cd8e1f6999c16d5473ac1ccc7b74906b2cb9dde76a38',
        email='riki@riki.com',
        bio='hi im riki',
    )
    user2 = User(
        username='Riki2',
        hashed_password='pbkdf2:sha256:150000$ltOXv3W8$6e1e42bfc60f89dde0a8cd8e1f6999c16d5473ac1ccc7b74906b2cb9dde76a38',
        email='ema243il2@email.com',
        bio='bio2 good',
    )
    user3 = User(
        username='Jimbo',
        hashed_password='pbkdf2:sha256:150000$ltOXv3W8$6e1e42bfc60f89dde0a8cd8e1f6999c16d5473ac1ccc7b74906b2cb9dde76a38',
        email='jimbo@email.com',
        bio='I am a professional photographer',
    )
    user4 = User(
        username='Guest',
        hashed_password='pbkdf2:sha256:150000$ltOXv3W8$6e1e42bfc60f89dde0a8cd8e1f6999c16d5473ac1ccc7b74906b2cb9dde76a38',
        email='guest@guest.com',
        bio='hi im a guest! ',
    )
    f1 = Follow(
        follower=user1,
        followed=user2,
    )
    f2 = Follow(
        follower=user2,
        followed=user1,
    )
    f3 = Follow(
        follower=user4,
        followed=user1
    )
    f4 = Follow(
        follower=user4,
        followed=user2,
    )
    f5 = Follow(
        follower=user4,
        followed=user3,
    )

    post1 = Post(
        image='https://res.cloudinary.com/dgzcv1mcs/image/upload/v1589790758/Soundzone/images_uh1rxq.jpg',
        caption='Ravesignal III',
        poster=user1,
    )
    post2 = Post(
        image='https://res.cloudinary.com/dgzcv1mcs/image/upload/v1589789244/Soundzone/a1139886656_10_ckmxu3.jpg',
        caption='Analphabetapolothology',
        poster=user1,
    )
    post3 = Post(
        image='https://res.cloudinary.com/dgzcv1mcs/image/upload/v1589789439/Soundzone/a0265977949_10_sssren.jpg',
        caption='Chanel Beads',
        poster=user1,
    )
    post4 = Post(
        image='https://res.cloudinary.com/dgzcv1mcs/image/upload/v1589788191/Soundzone/Sugar_is_Sweeter_hddwkc.jpg',
        caption='Sugar is Sweeter - Jeff Mills',
        poster=user1,
    )
    post5 = Post(
        image='https://res.cloudinary.com/dgzcv1mcs/image/upload/v1589789905/Soundzone/a0856938911_10_c8x7h7.jpg',
        caption='Grouper - Ruins',
        poster=user1,
    )
    post6 = Post(
        image='https://res.cloudinary.com/dgzcv1mcs/image/upload/v1591832875/Instantelegram/tree-736885_960_720_dmz2j3.jpg',
        caption='Amazing Tree',
        poster=user3,
    )
    post7 = Post(
        image='https://res.cloudinary.com/dgzcv1mcs/image/upload/v1591832875/Instantelegram/aya-sofia-915076_960_720_avru8o.jpg',
        caption='Aya Sofia',
        poster=user3,
    )
    post8 = Post(
        image='https://res.cloudinary.com/dgzcv1mcs/image/upload/v1591832876/Instantelegram/venice-3118803_960_720_eslila.jpg',
        caption='Venice Palace,
        poster=user3,
    )
    post9 = Post(
        image='https://res.cloudinary.com/dgzcv1mcs/image/upload/v1591832876/Instantelegram/sea-5237374_960_720_vikixv.jpg',
        caption='Beautiful Ocean',
        poster=user3,
    )
    like1 = PostLike(
        post_liked=post6
        post_liker=user1
    )
    like2 = PostLike(
        post_liked=post7
        post_liker=user1
    )
    like3 = PostLike(
        post_liked=post8
        post_liker=user1
    )
    like4 = PostLike(
        post_liked=post9
        post_liker=user1
    )

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(f1)
    db.session.add(f2)
    db.session.add(f3)
    db.session.add(f4)
    db.session.add(f5)
    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)
    db.session.add(post4)
    db.session.add(post5)
    db.session.add(post6)
    db.session.add(post7)
    db.session.add(post8)
    db.session.add(post9)
    db.session.add(like1)
    db.session.add(like2)
    db.session.add(like3)
    db.session.add(like4)
    db.session.commit()
