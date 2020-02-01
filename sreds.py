import praw
import pandas as pd

def main():
    subreddits = []
    posts = []
       
    client_id = ''
    client_secret = ''
    user_name = ''

    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_name)

    keyWords_input = input('Key words(separate them with a \', \'): ')
    
    keyWords = keyWords_input.split(', ')
    #add key words for the search
    
    subreddits_input = input('Subreddits(separate them with a \', \'): ') 
    subreddits = subreddits_input.split(', ')
    
    for i in range(len(subreddits)):
        subreddits[i] = reddit.subreddit(subreddits[i]) #transform the strings into subreddit objects
    
    for subreddit in subreddits:
        try:
            for post in subreddit.hot(limit=20):
                for keyWord in keyWords:
                    if (keyWord in post.title) == True:#see if the title has one or more keyWords
                        posts.append([keyWord, 'r/{}'.format(subreddit.display_name), post.title, post.url])#get the subreddit's name, the 5 hottests posts titles and urls
        #add a title from a post only if it has a key word
        except praw.exceptions.APIException:#if the subreddit was not found
            print('{} not found'.format(subreddit.display_name))

    if len(posts) > 0:
        #transforms the gotten posts' titles and urls into a data frame
        posts = pd.DataFrame(posts, columns = ['keyWord', 'subreddit', 'post_title', 'post_url'])
        posts.to_csv('output.csv')
        print('done!')
    else:
        print('no posts found')
        

if __name__ == '__main__':
    main()
