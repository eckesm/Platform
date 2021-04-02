# from app.models import db, connect_db, generate_random_integer, User, Group, Membership, Post, CommentType, CommentType, AWSFileStorage
from app.models import db, generate_random_integer, User, Group, Membership, Post, CommentType, CommentType, AWSFileStorage
from sqlalchemy.sql import func

from wsgi import create_app
app = create_app()


def reseed_main_database():

    # Add and commit users.
    user1 = User(first_name='Matthew',
                 last_name='Eckes',
                 email_address='meckes@gmail.com',
                 is_email_confirmed=True,
                 username='meckes',
                 password='$2b$14$ignR7XzBdrwlY.0yUExVnuqSKx5iYMEMNM3o7CRDIb5y.1DOXdY7q',
                 subject_pronoun='he',
                 object_pronoun='him',
                 profile_image_id='klb9kosj3x73zfatbhurp95tw',
                 role='administrator',
                 api_token=User.generate_api_token(),
                 app_privileges='{"EUROVISION_MGMT":{"role":"admin","name":"Eurovision API","href":"/eurovision/manage"}}')
    user2 = User(first_name='John',
                 last_name='Latchaw',
                 email_address='jlatchaw@gmail.com',
                 is_email_confirmed=True,
                 username='jlatchaw',
                 password='$2b$14$PYJbEjsK.ubTXylyALrmd.rBEhG6ODiocjKFV39FiZYv1JxMxD8ai',
                 subject_pronoun='he',
                 object_pronoun='him',
                 profile_image_id='nxew011f4kcr7ngcbhjedrwdy',
                 header_image_url='https://images.unsplash.com/photo-1479502806991-251c94be6b15?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxleHBsb3JlLWZlZWR8MTN8fHxlbnwwfHx8&auto=format&fit=crop&w=500&q=60',
                 api_token=User.generate_api_token(),
                 app_privileges='{"EUROVISION_MGMT":{"role":"admin","name":"Eurovision API","href":"/eurovision/manage"}}')
    user3 = User(first_name='Laura',
                 last_name='Eckes',
                 email_address='leckes@gmail.com',
                 is_email_confirmed=True,
                 username='leckes',
                 password='$2b$14$VJw9jRDna9f6FK9ZtONw9u9aOyedmbnYUAR3jnvxJYyiL8T.mlBKC',
                 subject_pronoun='she',
                 object_pronoun='her',
                 #  profile_image_id='uploads/Laura Eckes.jpg',
                 header_image_url='https://images.unsplash.com/photo-1542293787938-c9e299b880cc?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxleHBsb3JlLWZlZWR8N3x8fGVufDB8fHw%3D&auto=format&fit=crop&w=500&q=60',
                 api_token=User.generate_api_token())
    user4 = User(first_name='Grace',
                 last_name='Thomson',
                 email_address='gthomson@gmail.com',
                 is_email_confirmed=True,
                 username='gthomson',
                 password='$2b$14$PLDgmzz7lepQUhWgqmSBTuRbWlaWCO8MGEXd6cm5YJYmlazmCnOLS',
                 subject_pronoun='she',
                 object_pronoun='her',
                 #  profile_image_id='uploads/Grace Thomson.jpg',
                 api_token=User.generate_api_token())
    user5 = User(first_name='Avi',
                 last_name='Steinbach',
                 email_address='asteinbach@gmail.com',
                 is_email_confirmed=True,
                 username='asteinbach',
                 profile_image_id='8j53bk7qqjpaui9gfbip692p0',
                 password='$2b$14$fqXpo9hc63GrQ0lOJjhw9uN9vhDHXiJomi4AVgJ8vlBIeOglAP9xC',
                 subject_pronoun='he',
                 object_pronoun='him',
                 api_token=User.generate_api_token())
    user6 = User(first_name='Penny',
                 last_name='Rosenberg',
                 email_address='prosenberg@gmail.com',
                 is_email_confirmed=True,
                 username='prosenberg',
                 password='$2b$14$sd4HFHqk/cgBKbgXn1LhIu9Gfr4TAzYOQOIwGtdrfxcnIElabVRlO',
                 subject_pronoun='she',
                 object_pronoun='her',
                 api_token=User.generate_api_token())
    user7 = User(first_name='Sue',
                 last_name='Young',
                 email_address='syoung@gmail.com',
                 is_email_confirmed=True,
                 username='syoung',
                 password='$2b$14$jConSG7gv8bc0/IBpa44we.Ro60bN6ifDpUqX4IfFyO6TTvi9AzKa',
                 subject_pronoun='she',
                 object_pronoun='her',
                 api_token=User.generate_api_token())
    user8 = User(first_name='John',
                 last_name='Eckes',
                 email_address='jeckes@gmail.com',
                 is_email_confirmed=True,
                 username='jeckes',
                 password='$2b$14$sH4ufPl548YM.xflwXoxWutrkd9cEtPfGB613fF.RxUd7FrvAclZq',
                 subject_pronoun='he',
                 object_pronoun='him',
                 api_token=User.generate_api_token())
    db.session.add_all([user1, user2, user3, user4,
                        user5, user6, user7, user8])
    db.session.commit()

    # Add and commit groups.
    group1 = Group(owner_id=user1.id,
                   name='Eckes Family',
                   description='The Eckes family and their significant others.')
    group2 = Group(owner_id=user3.id,
                   name='PBML',
                   description='Pots by Matt & Laura')
    group3 = Group(owner_id=user2.id,
                   name='Ahlgren/Latchaw Family',
                   description='The Ahlgren/Latchaw family and their significant others.')
    group4 = Group(owner_id=user4.id,
                   name='Alaska Bound!',
                   description='Solely devoted to remembering our trip to Alaska.')
    db.session.add_all([group1, group2, group3, group4])
    db.session.commit()

    # Add and commit memberships.
    membership1 = Membership(member_id=user1.id,
                             group_id=group1.id,
                             member_type='owner',
                             invited_by_id=user1.id,
                             joined=func.now())
    membership2 = Membership(member_id=user2.id,
                             group_id=group1.id,
                             member_type='member',
                             invited_by_id=user1.id,
                             joined=func.now())
    membership3 = Membership(member_id=user3.id,
                             group_id=group1.id,
                             member_type='member',
                             invited_by_id=user1.id,
                             joined=func.now())
    membership4 = Membership(member_id=user1.id,
                             group_id=group3.id,
                             member_type='member',
                             invited_by_id=user2.id,
                             joined=func.now())
    membership5 = Membership(member_id=user2.id,
                             group_id=group3.id,
                             member_type='owner',
                             invited_by_id=user2.id,
                             joined=func.now())
    membership6 = Membership(member_id=user3.id,
                             group_id=group2.id,
                             member_type='owner',
                             invited_by_id=user3.id,
                             joined=func.now())
    membership7 = Membership(member_id=user1.id,
                             group_id=group2.id,
                             member_type='member',
                             invited_by_id=user3.id,
                             joined=func.now())
    membership8 = Membership(member_id=user5.id,
                             group_id=group1.id,
                             member_type='invited',
                             invited_by_id=user1.id,
                             joined=func.now())
    membership9 = Membership(member_id=user6.id,
                             group_id=group1.id,
                             member_type='invited',
                             invited_by_id=user1.id,
                             joined=func.now())
    membership10 = Membership(member_id=user4.id,
                              group_id=group4.id,
                              member_type='owner',
                              invited_by_id=user4.id,
                              joined=func.now())
    membership11 = Membership(member_id=user1.id,
                              group_id=group4.id,
                              member_type='member',
                              invited_by_id=user4.id,
                              joined=func.now())
    membership12 = Membership(member_id=user2.id,
                              group_id=group4.id,
                              member_type='member',
                              invited_by_id=user4.id,
                              joined=func.now())
    membership13 = Membership(member_id=user3.id,
                              group_id=group4.id,
                              member_type='member',
                              invited_by_id=user4.id,
                              joined=func.now())
    membership14 = Membership(member_id=user5.id,
                              group_id=group4.id,
                              member_type='member',
                              invited_by_id=user4.id,
                              joined=func.now())
    membership15 = Membership(member_id=user6.id,
                              group_id=group4.id,
                              member_type='member',
                              invited_by_id=user4.id,
                              joined=func.now())
    membership16 = Membership(member_id=user7.id,
                              group_id=group4.id,
                              member_type='member',
                              invited_by_id=user4.id,
                              joined=func.now())
    membership17 = Membership(member_id=user8.id,
                              group_id=group1.id,
                              member_type='member',
                              invited_by_id=user1.id,
                              joined=func.now())
    membership18 = Membership(member_id=user8.id,
                              group_id=group4.id,
                              member_type='member',
                              invited_by_id=user4.id,
                              joined=func.now())
    db.session.add_all([membership1, membership2, membership3,
                        membership4, membership5, membership6, membership7, membership8, membership9, membership10, membership11, membership12, membership13, membership14, membership15, membership16, membership17, membership18])
    db.session.commit()

    # Add and commit posts
    post1 = Post(owner_id=user1.id,
                 group_id=group1.id,
                 content="We should do something for Penny's 65th birthday!")
    post2 = Post(owner_id=user3.id,
                 group_id=group1.id,
                 content="Agreed--she will be disappointed  if we don't.")
    post3 = Post(owner_id=user2.id,
                 group_id=group1.id,
                 content="I'm in!")
    post4 = Post(owner_id=user1.id,
                 group_id=group1.id,
                 content="Okay I will talk to John Eckes about it and see if we can figure something out.  Hopefully he has some ideas and is willing to do something fun at the house.")
    post5 = Post(owner_id=user2.id,
                 group_id=group1.id,
                 content="I will pick up a cake on my way over.")
    post6 = Post(owner_id=user3.id,
                 group_id=group1.id,
                 content="Oh wait! I think this is actually just her 64th birthday.  So maybe it's not such a big deal if it's not like a big party???")
    post7 = Post(owner_id=user1.id,
                 group_id=group1.id,
                 content="Hmm... okay well then maybe we just go over for dinner and be really nice to her.  She normally appreciates when we are uncharacteristically nice for extended periods of time haha.")
    post8 = Post(owner_id=user2.id,
                 group_id=group1.id,
                 content="Hahahahaha")
    db.session.add_all([post1, post2, post3, post4,
                        post5, post6, post7, post8])
    db.session.commit()

    image1 = AWSFileStorage(id='klb9kosj3x73zfatbhurp95tw',
                            owner_id=user1.id,
                            url='https://mre-platform.s3.us-east-2.amazonaws.com/klb9kosj3x73zfatbhurp95tw.jpg',
                            file_type='image',
                            category='profile-picture')
    image2 = AWSFileStorage(id='nxew011f4kcr7ngcbhjedrwdy',
                            owner_id=user2.id,
                            url='https://mre-platform.s3.us-east-2.amazonaws.com/nxew011f4kcr7ngcbhjedrwdy.jpg',
                            file_type='image',
                            category='profile-picture')
    image3 = AWSFileStorage(id='8j53bk7qqjpaui9gfbip692p0',
                            owner_id=user4.id,
                            url='https://mre-platform.s3.us-east-2.amazonaws.com/8j53bk7qqjpaui9gfbip692p0.jpg',
                            file_type='image',
                            category='profile-picture')
    db.session.add_all([image1, image2, image3])
    db.session.commit()


with app.app_context():
    db.drop_all()
    db.create_all()
    reseed_main_database()
