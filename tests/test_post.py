import unittest
from app.models import Post, User


class PostTest(unittest.TestCase):
    '''
    Test class to test the behaviour of the Post class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_post = Post("hello","We are the posts","kimonyoski")

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post,Post))
