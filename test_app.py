from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = True

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users/Posts"""

    def setUp(self):
        """Clean up any existing users/posts"""
        Post.query.delete()
        User.query.delete()

        """Add sample user"""
        user = User(first_name="Eloise", last_name="Bridgerton", image_url="https://assets.popbuzz.com/2021/01/how-old-is-eloise-from-bridgerton---claudia-jessie-1609943404-view-0.jpg")
        db.session.add(user)
        db.session.commit()

        self.user = user
        self.user_id = user.id   
        self.name = f"{user.first_name} {user.last_name}"     
        
        """Add sample post"""
        post = Post(title = "Lady Whistledown is...", content = "Lady Danbury!", user_id = self.user_id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.post = post
        self.title = post.title
        
    
    def tearDown(self):
        """Clean up any fouled transactions."""
        db.session.rollback()
    
    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.name, html)

    def test_new_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<button class = 'btn btn-warning'>Create User</button>", html)

    def test_add_user(self):
        with app.test_client() as client:
            data = {"first_name": "Lady", "last_name": "Whistledown", "image_url": "'https://cvhrma.org/wp-content/uploads/2015/07/default-profile-photo.jpg'"}
            resp = client.post("/users/new", data = data, follow_redirects = True )
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h3>Lady Whistledown</h3>", html)
    
    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<h3>{self.name}</h3>", html)
            
    def test_list_posts(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.title, html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/{self.post_id}')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<h3>{self.title}</h3>", html)
    
    def test_add_post(self):
        with app.test_client() as client:
            data = {"user_id": self.user_id, "title": "Who Lady Whistledown Is Not...", "content": "A maid, they don't have the time!"}
            resp = client.post(f"/users/{self.user_id}/posts/new", data = data, follow_redirects = True )
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h3>Who Lady Whistledown Is Not...</h3>", html)
    

    

    
