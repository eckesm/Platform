from app.models import db, generate_random_integer, User, Group, Membership, Post, CommentType, CommentType, AWSFileStorage
from sqlalchemy.sql import func


from wsgi import create_app
app = create_app()


def reseed_main_database():

    # Add and commit users.
    user1 = User.register(first_name='Matthew',
                          last_name='Eckes',
                          email_address='eckesm@gmail.com',
                          username='meckes',
                          password='passwordmeckes')
    user1.is_email_confirmed = True
    user1.subject_pronoun = 'he'
    user1.object_pronoun = 'him'
    user1.profile_image_id = 'klb9kosj3x73zfatbhurp95tw'
    user1.role = 'administrator'
    user1.app_privileges = '{"EUROVISION_MGMT":{"role":"admin","name":"Eurovision API","href":"/eurovision/manage"}}'

    user2 = User.register(first_name='John',
                          last_name='Latchaw',
                          email_address='jlatchaw@gmail.com',
                          username='jlatchaw',
                          password='passwordjlatchaw')
    user2.is_email_confirmed = True
    user2.subject_pronoun = 'he'
    user2.object_pronoun = 'him'
    user2.profile_image_id = 'nxew011f4kcr7ngcbhjedrwdy'
    user2.header_image_url = 'https://images.unsplash.com/photo-1479502806991-251c94be6b15?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxleHBsb3JlLWZlZWR8MTN8fHxlbnwwfHx8&auto=format&fit=crop&w=500&q=60'
    user2.app_privileges = '{"EUROVISION_MGMT":{"role":"admin","name":"Eurovision API","href":"/eurovision/manage"}}'

    user3 = User.register(first_name='Laura',
                          last_name='Eckes',
                          email_address='leckes@gmail.com',
                          username='leckes',
                          password='passwordleckes')
    user3.is_email_confirmed = True
    user3.profile_image_id = 'azwonxkk1w0v40y38bgfhqcih'
    user3.subject_pronoun = 'she'
    user3.object_pronoun = 'her'
    user3.header_image_url = 'https://images.unsplash.com/photo-1542293787938-c9e299b880cc?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxleHBsb3JlLWZlZWR8N3x8fGVufDB8fHw%3D&auto=format&fit=crop&w=500&q=60'

    user4 = User.register(first_name='Grace',
                          last_name='Thomson',
                          email_address='gthomson@gmail.com',
                          username='gthomson',
                          password='passwordgthomson')
    user4.is_email_confirmed = True
    user4.profile_image_id = 'cvn71f8v63b5quuftp5858thp'
    user4.subject_pronoun = 'she'
    user4.object_pronoun = 'her'

    user5 = User.register(first_name='Avi',
                          last_name='Steinbach',
                          email_address='asteinbach@gmail.com',
                          username='asteinbach',
                          password='passwordasteinbach')
    user5.is_email_confirmed = True
    user5.profile_image_id = '8j53bk7qqjpaui9gfbip692p0'
    user5.subject_pronoun = 'he'
    user5.object_pronoun = 'him'

    user6 = User.register(first_name='Penny',
                          last_name='Rosenberg',
                          email_address='prosenberg@gmail.com',
                          username='prosenberg',
                          password='passwordprosenberg')
    user6.is_email_confirmed = True
    user6.subject_pronoun = 'she'
    user6.object_pronoun = 'her'

    user7 = User.register(first_name='Sue',
                          last_name='Young',
                          email_address='syoung@gmail.com',
                          username='syoung',
                          password='passwordsyoung')
    user7.is_email_confirmed = True
    user7.subject_pronoun = 'she'
    user7.object_pronoun = 'her'

    user8 = User.register(first_name='John',
                          last_name='Eckes',
                          email_address='jeckes@gmail.com',
                          username='jeckes',
                          password='passwordjeckes')
    user8.is_email_confirmed = True
    user8.subject_pronoun = 'he'
    user8.object_pronoun = 'him'

    db.session.add_all([user1, user2, user3, user4,
                        user5, user6, user7, user8])
    db.session.commit()

    # Add and commit groups.
    group1 = Group.register(owner_id=user1.id,
                            name='Eckes Family',
                            description='The Eckes family and their significant others.',
                            members_add_users=False)
    group2 = Group.register(owner_id=user3.id,
                            name='PBML',
                            description='Pots by Matt & Laura',
                            members_add_users=True)
    group3 = Group.register(owner_id=user2.id,
                            name='Ahlgren/Latchaw Family',
                            description='The Ahlgren/Latchaw family and their significant others.',
                            members_add_users=False)
    group4 = Group.register(owner_id=user4.id,
                            name='Alaska Bound!',
                            description='Solely devoted to remembering our trip to Alaska.',
                            members_add_users=True)
    # db.session.add_all([group1, group2, group3, group4])
    # db.session.commit()

    # Add and commit memberships.
    membership1 = Membership.register(member_id=user1.id,
                                      group_id=group1.id,
                                      member_type='owner',
                                      invited_by_id=user1.id,
                                      joined=func.now())
    membership2 = Membership.register(member_id=user2.id,
                                      group_id=group1.id,
                                      member_type='member',
                                      invited_by_id=user1.id,
                                      joined=func.now())
    membership3 = Membership.register(member_id=user3.id,
                                      group_id=group1.id,
                                      member_type='member',
                                      invited_by_id=user1.id,
                                      joined=func.now())
    membership4 = Membership.register(member_id=user1.id,
                                      group_id=group3.id,
                                      member_type='member',
                                      invited_by_id=user2.id,
                                      joined=func.now())
    membership5 = Membership.register(member_id=user2.id,
                                      group_id=group3.id,
                                      member_type='owner',
                                      invited_by_id=user2.id,
                                      joined=func.now())
    membership6 = Membership.register(member_id=user3.id,
                                      group_id=group2.id,
                                      member_type='owner',
                                      invited_by_id=user3.id,
                                      joined=func.now())
    membership7 = Membership.register(member_id=user1.id,
                                      group_id=group2.id,
                                      member_type='member',
                                      invited_by_id=user3.id,
                                      joined=func.now())
    membership8 = Membership.register(member_id=user5.id,
                                      group_id=group1.id,
                                      member_type='invited',
                                      invited_by_id=user1.id,
                                      joined=func.now())
    membership9 = Membership.register(member_id=user6.id,
                                      group_id=group1.id,
                                      member_type='invited',
                                      invited_by_id=user1.id,
                                      joined=func.now())
    membership10 = Membership.register(member_id=user4.id,
                                       group_id=group4.id,
                                       member_type='owner',
                                       invited_by_id=user4.id,
                                       joined=func.now())
    membership11 = Membership.register(member_id=user1.id,
                                       group_id=group4.id,
                                       member_type='member',
                                       invited_by_id=user4.id,
                                       joined=func.now())
    membership12 = Membership.register(member_id=user2.id,
                                       group_id=group4.id,
                                       member_type='member',
                                       invited_by_id=user4.id,
                                       joined=func.now())
    membership13 = Membership.register(member_id=user3.id,
                                       group_id=group4.id,
                                       member_type='member',
                                       invited_by_id=user4.id,
                                       joined=func.now())
    membership14 = Membership.register(member_id=user5.id,
                                       group_id=group4.id,
                                       member_type='member',
                                       invited_by_id=user4.id,
                                       joined=func.now())
    membership15 = Membership.register(member_id=user6.id,
                                       group_id=group4.id,
                                       member_type='member',
                                       invited_by_id=user4.id,
                                       joined=func.now())
    membership16 = Membership.register(member_id=user7.id,
                                       group_id=group4.id,
                                       member_type='member',
                                       invited_by_id=user4.id,
                                       joined=func.now())
    membership17 = Membership.register(member_id=user8.id,
                                       group_id=group1.id,
                                       member_type='member',
                                       invited_by_id=user1.id,
                                       joined=func.now())
    membership18 = Membership.register(member_id=user8.id,
                                       group_id=group4.id,
                                       member_type='member',
                                       invited_by_id=user4.id,
                                       joined=func.now())
    # db.session.add_all([membership1, membership2, membership3,
    #                     membership4, membership5, membership6, membership7, membership8, membership9, membership10, membership11, membership12, membership13, membership14, membership15, membership16, membership17, membership18])
    # db.session.commit()

    # Add and commit posts
    post1 = Post.register(owner_id=user1.id,
                          group_id=group1.id,
                          content="We should do something for Penny's 65th birthday!")
    post2 = Post.register(owner_id=user3.id,
                          group_id=group1.id,
                          content="Agreed--she will be disappointed  if we don't.")
    post3 = Post.register(owner_id=user2.id,
                          group_id=group1.id,
                          content="I'm in!")
    post4 = Post.register(owner_id=user1.id,
                          group_id=group1.id,
                          content="Okay I will talk to John Eckes about it and see if we can figure something out.  Hopefully he has some ideas and is willing to do something fun at the house.")
    post5 = Post.register(owner_id=user2.id,
                          group_id=group1.id,
                          content="I will pick up a cake on my way over.")
    post6 = Post.register(owner_id=user3.id,
                          group_id=group1.id,
                          content="Oh wait! I think this is actually just her 64th birthday.  So maybe it's not such a big deal if it's not like a big party???")
    post7 = Post.register(owner_id=user1.id,
                          group_id=group1.id,
                          content="Hmm... okay well then maybe we just go over for dinner and be really nice to her.  She normally appreciates when we are uncharacteristically nice for extended periods of time haha.")
    post8 = Post.register(owner_id=user2.id,
                          group_id=group1.id,
                          content="Hahahahaha")
    # db.session.add_all([post1, post2, post3, post4,
    #                     post5, post6, post7, post8])
    # db.session.commit()

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

    image3 = AWSFileStorage(id='azwonxkk1w0v40y38bgfhqcih',
                            owner_id=user3.id,
                            url='https://mre-platform.s3.us-east-2.amazonaws.com/azwonxkk1w0v40y38bgfhqcih.jpg',
                            file_type='image',
                            category='profile-picture')
    image4 = AWSFileStorage(id='cvn71f8v63b5quuftp5858thp',
                            owner_id=user4.id,
                            url='https://mre-platform.s3.us-east-2.amazonaws.com/cvn71f8v63b5quuftp5858thp.jpg',
                            file_type='image',
                            category='profile-picture')
    image5 = AWSFileStorage(id='8j53bk7qqjpaui9gfbip692p0',
                            owner_id=user4.id,
                            url='https://mre-platform.s3.us-east-2.amazonaws.com/8j53bk7qqjpaui9gfbip692p0.jpg',
                            file_type='image',
                            category='profile-picture')

    db.session.add_all([image1, image2, image3, image4, image5])
    db.session.commit()


with app.app_context():
    db.drop_all()
    db.create_all()
    reseed_main_database()
