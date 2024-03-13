from app import app
import unittest

# Test get and post routes for "/"
# Test get and post routes for "/user/edit"
# Test get route for "/user/delete"


class AppTest(unittest.TestCase):


    def homepage_get_route(self):
        resp = app.get('/')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<span>Blogly</span>', html)

    def homepage_post_route(self):
        resp = app.post('/', 
                        data={'first_name': 'test',
                                'last_name': 'testington'})
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<div class="alert alert-success">User Succesfully Updated</div>', html)


if __name__ == '__main__':
    unittest.main()