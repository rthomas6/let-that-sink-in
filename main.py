import praw
import toml
import random

config = toml.load('config.toml')

reddit = praw.Reddit(
        client_id = config['client_id'],
        client_secret = config['client_secret'],
        user_agent = config['user_agent'],
        username = config['username'],
        password = config['password']
        )

def make_sentence():
    sink = random.choice(['it', 'he', 'that sink'])
    #preface = random.choice(['', 'Again? ', '>Let that sink in\n\n'])
    preface = random.choice(['', 'Again? '])
    query = random.choice(['What', 'What the hell', 'What the fuck', 'The hell', 'The fuck'])
    time = random.choice([' now', ' this time', ''])
    intention = random.choice([f' does {sink} want{time}', f' is {sink} doing here{time}'])
    link_sentence = ''.join([query, intention])
    return f'{preface}[{link_sentence}?](https://i.imgur.com/MDhbuT6.jpg)'

def match(comment, end_region = 100000):
    if comment.author != config['username']:
        if 'Let that sink in' in comment.body[(-1 * end_region):]:
            return True
    return False

for comment in reddit.subreddit('all').stream.comments():
    if match(comment):
        #If phrase in last 50 chars
        if match(comment, 50):
            comment.reply(make_sentence())
        else:
            comment.reply('>Let that sink in\n\n' + make_sentence())
        print(f'https://www.reddit.com{comment.permalink}')
