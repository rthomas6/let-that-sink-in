import praw
import prawcore
import toml
import random
import functools

config = toml.load('config.toml')

reddit = praw.Reddit(
        client_id = config['client_id'],
        client_secret = config['client_secret'],
        user_agent = config['user_agent'],
        username = config['username'],
        password = config['password']
        )

def handle_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (prawcore.exceptions.Forbidden, prawcore.exceptions.ServerError) as error:
            print(f'Error when calling {func.__name__} ({error}). Resuming...')
            return wrapper(*args, **kwargs)
    return wrapper

def make_sentence():
    sink = random.choice(['it', 'he', 'that sink'])
    #preface = random.choice(['', 'Again? ', '>Let that sink in\n\n'])
    preface = random.choice(['', 'Again? ', 'Seriously? '])
    what = random.choice(['What', 'What the hell', 'What the fuck', 'The hell', 'The fuck'])
    where = random.choice(['Where', 'Where the hell', 'Where the fuck', 'The hell', 'The fuck'])
    time = random.choice([' now', ' this time', ''])
    link_sentence = random.choice([f'{what} does {sink} want{time}', f'{what} is {sink} doing here{time}', f'{where} did that sink come from'])
    #link_sentence = ''.join([query, intention])
    return f'{preface}[{link_sentence}?](https://i.imgur.com/MDhbuT6.jpg)'

def match(comment, end_region = 2000):
    if comment.author != config['username']:
        if 'Let that sink in' in comment.body[(-1 * end_region):]:
            return True
    return False

def make_comment_if_match(comment):
    if match(comment):
        #If phrase in last 50 chars
        if match(comment, 50):
            comment.reply(make_sentence())
        else:
            comment.reply('>Let that sink in\n\n' + make_sentence())

@handle_exceptions
def search_all_comments():
    for comment in reddit.subreddit('all').stream.comments():
        try:
            make_comment_if_match(comment)
        except prawcore.exceptions.Forbidden:
            print(f'403 Forbidden when replying to: https://www.reddit.com{comment.permalink}')

search_all_comments()
