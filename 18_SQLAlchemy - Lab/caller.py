from main import engine, Session
from models import User, Order

session = Session()

# 1. Creating one user
# with Session() as session:
#     user = User(
#         username='John_adams',
#         email='john.adams@yahoo.co.uk'
#     )
#
#     session.add(user)
#     session.commit()

# 2. Printing all user in the data base
# with Session() as session:
#     users = session.query(User).all()
#
#     for user in users:
#         print(user.username, user.email)

# 3. Finding the first user with the username, printing that he updated his email or user not found
# with Session() as session:
#     user_to_update = session.query(User).filter_by(username='john_doe').first()
#
#     if user_to_update:
#         user_to_update.email = 'doe.john@yahoo.com'
#         session.commit()
#         print(f'User {user_to_update.username} has updated his email to {user_to_update.email}')
#     else:
#         print("User not found!")

# 4. Finding the first user with the username and deleting him if he exists
# with Session() as session:
#     user_to_delete = session.query(User).filter_by(username='john_doe').first()
#
#     if user_to_delete:
#         session.delete(user_to_delete)
#         session.commit()
#         print(f'User deleted successfully')
#     else:
#         print("User not found!")

# 5. Making a transaction to delete all the user if error happens,
# # we roll back to the previous stage of the database and at the end we close the session
# try:
#     session.begin()
#     session.query(User).delete()
#     session.commit()
#     print('All user deleted successfully')
# except Exception as e:
#     session.rollback()
#     print('An error occurred', str(e))
# finally:
#     session.close()

# 6. Added 2 orders and making a relationship between the two tables
# with Session() as active_session:
#     active_session.add(Order(user_id=6), Order(user_id=7))
#     active_session.commit()