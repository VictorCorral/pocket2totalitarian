#!/usr/bin/env python
# coding=utf-8
import pocket, requests
from pprint import pprint
class PocketTag():
    def __init__(self, tag, consumer_key, access_token):
        self.p = pocket.Pocket(consumer_key, access_token)

        self.tag = tag
        self.__retrieve_tag()
    def __retrieve_tag(self):
        self.articles = self.p.get(tag=self.tag)[0]['list']
        return self
    def get_tag(self):
        return self.tag
    def title_url(self):
        if type(self.articles) == type(dict()):
            self.title2url =  map(lambda x: 
                   {'id': x['item_id'],
                    'title': x['resolved_title'],
                    'url': x['given_url'] 
                   }, self.articles.values())
            return True
        else:
            return False

class Totalitarian():
    def __init__(self, username, password):
        self.session = requests.session()
        self.session.post("https://www.totalitarian.info/login",
                              {'email':username,'password':password},
                              verify=False)
    def submit(self, url, title, tag):
        s = self.session.post('https://www.totalitarian.info/stories',
                          {'story[url]' : url,
                           'story[title]': title,
                           'story[tags_a][]': tag,
                           'story[anon]': '0',
                           'commit': 'submit'
                          },
                          verify=False
                         )
        return True
        
if __name__ == '__main__':
    totalitarian_username = 'username'
    totalitarian_password = 'password'
    consumer_key = 'ck'
    access_token = 'at'

    tags = [
        'fa',
        'g',
        'lit',
        'mu',
        'prog',
        'r9k',
        'sci',
        'v'
    ]
    for tag in tags:
        p = PocketTag(tag, consumer_key, access_token)
        t = Totalitarian(totalitarian_username, totalitarian_password)
        if p.title_url():
            for link in p.title2url:
                print link['title'],
                t.submit(link['url'], link['title'], p.get_tag())
                print 'SUBMTITED'
        else:
            print p.tag, ': No articles found'
