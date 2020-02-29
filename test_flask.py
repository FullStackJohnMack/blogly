from app import app
from models import db, User, Tag
from unittest import TestCase

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for User."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="John", last_name="Mack", image_url="https://picsum.photos/200/300")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """Tests to see if home page displays users as expected"""
        with app.test_client() as client:
            resp = client.get("/",follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Mack', html)

    def test_show_users(self):
        """Tests if a user page is correctly loading"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>John Mack</h1>', html)

    def test_add_user(self):
        """Tests if a new user is successfully added"""
        with app.test_client() as client:
            d = {"first_name": "Elisha", "last_name": "Mack", "image_url": "https://picsum.photos/200/300"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Elisha Mack", html)

class TagViewsTestCase(TestCase):
    """Tests for views for Tag."""

    def setUp(self):
        """Add sample user."""

        Tag.query.delete()

        tag = Tag(name="Test Tag")
        db.session.add(tag)
        db.session.commit()

        self.tag_id = tag.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_add_tag(self):
        """Tests that a tag was created"""
        with app.test_client() as client:
            d = {"name": "Yo Yo Ma"}
            resp = client.post("/tags/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Yo Yo Ma</a>", html)
    
    def test_delete_tag(self):
        """Tests if a tag was deleted including from database"""
        with app.test_client() as client:
            test = Tag.query.all()
            self.assertEquals(len(test),1)
            resp = client.get(f"/tags/{self.tag_id}/delete")
            test = Tag.query.all()
            self.assertEquals(len(test),0)
