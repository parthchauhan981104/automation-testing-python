from unittest import TestCase
try:
    from unittest.mock import patch
    #to be able to test the printed output in console, we patch the print function
    #used for faking regular functions. patching a function replaces it for a mock.
except ImportError:
    from mock import patch

from blog import appp
from blog.blog import Blog
from blog.post import Post

#we check if functions are calling other functions as long as they have the value they expect

class AppTest(TestCase):
    def setUp(self):
        blog = Blog('Test', 'Test Author')
        appp.blogs = {'Test': blog}

    def test_menu_prints_blogs(self):
        with patch('builtins.print') as mocked_print:
            with patch('builtins.input', return_value='q'):
                appp.menu()
                #the original print is replace by this mocked_print function
                #asser_called_with check if the print function was called with this argument
                mocked_print.assert_called_with('- Test by Test Author (0 posts)')


    def test_menu_prints_prompt(self):
        with patch('builtins.input', return_value='q') as mocked_input:
            appp.menu()

            mocked_input.assert_called_with(appp.MENU_PROMPT)

    def test_menu_calls_create_blog(self):
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('c', 'Test Two', 'Test Author Two', 'q')
            appp.menu()

            self.assertIsNotNone(appp.blogs['Test Two'])

    def test_menu_calls_print_blogs(self):
        with patch('builtins.input') as mocked_input:
            with patch('blog.appp.print_blogs') as mocked_print_blogs:
                mocked_input.side_effect = ('l', 'q')
                appp.menu()

                mocked_print_blogs.assert_called()

    def test_menu_calls_ask_read_blogs(self):
        with patch('builtins.input') as mocked_input:
            with patch('blog.appp.ask_read_blog') as mocked_ask_read_blog:
                mocked_input.side_effect = ('r', 'Test', 'q')
                appp.menu()

                mocked_ask_read_blog.assert_called()

    def test_menu_calls_ask_create_post(self):
        with patch('builtins.input') as mocked_input:
            with patch('blog.appp.ask_create_post') as mocked_ask_create_post:
                mocked_input.side_effect = ('p', 'Test', 'New Post', 'New Content', 'q')
                appp.menu()

                mocked_ask_create_post.assert_called()

    def test_print_blogs(self):
        with patch('builtins.print') as mocked_print:
            appp.print_blogs()
            mocked_print.assert_called_with('- Test by Test Author (0 posts)')

    def test_ask_create_blog(self):
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('Test', 'Author')
            #side_effect return "Test" when function is called first time
            #returns "Author" when it is called second time. can similarly add more side effects.

            appp.ask_create_blog()

            self.assertIsNotNone(appp.blogs.get('Test'))
            self.assertEqual(appp.blogs.get('Test').title, 'Test')
            self.assertEqual(appp.blogs.get('Test').author, 'Author')

    def test_ask_read_blog(self):
        with patch('builtins.input', return_value='Test'):
            with patch('blog.appp.print_posts') as mocked_print_posts:
                appp.ask_read_blog()

                mocked_print_posts.assert_called_with(appp.blogs['Test'])

    def test_print_posts(self):
        blog = appp.blogs['Test']
        blog.create_post('Post title', 'Post content')

        with patch('blog.appp.print_post') as mocked_print_post:
            appp.print_posts(blog)

            mocked_print_post.assert_called_with(blog.posts[0])

    def test_print_post(self):
        post = Post('Post title', 'Post content')
        expected_print = """
--- Post title ---

Post content

"""

        with patch('builtins.print') as mocked_print:
            appp.print_post(post)

            mocked_print.assert_called_with(expected_print)

    def test_ask_create_post(self):
        blog = appp.blogs['Test']
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('Test', 'Test Title', 'Test Content')

            appp.ask_create_post()

            self.assertEqual(blog.posts[0].title, 'Test Title')
            self.assertEqual(blog.posts[0].content, 'Test Content')
