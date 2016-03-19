import praw
import re
import shelve
import sys
import time
from datetime import datetime

REDDIT_USERNAME = "" # username of the bot
REDDIT_PASS = "" # password of the bot
SUBREDDIT_NAME = "pvzgardenwarfare" # subreddit you wish to track
WAIT_TIME = 10 # seconds between checking the post for new users
POST_TITLE = "Definitive /r/pvzgardenwarfare Player List!" # Title of post the bot will create upon first activation
POST_HEADER = "Use [XBO] USERNAMEHERE for registering your username on the Xbox One. Use [PS4] USERNAMEHERE for registering your username on the Playstation 4. Use [ORIGIN] USERNAMEHERE for registering your username on PC." # Text you want to show up in the post before the lists of people

currentDirectory = sys.path[0] + "\\"
d = shelve.open(currentDirectory + 'pvzbot', flag='c', writeback=True)


def main():
    currentTime = '[' + str(datetime.now().strftime("%H:%M:%S")) + '] '
    print(str(currentTime) + 'Logging in...')
    r = praw.Reddit(user_agent = 'pvz user manager v0.1')
    already_done = []
    r.login(REDDIT_USERNAME, REDDIT_PASS, disable_warning = True)
    try:
        d['post_id']
        post = r.get_submission(submission_id=d['post_id'])
    except:
        print("Issue: No currently-logged post ID, time to make the thread...")
        post = r.submit(SUBREDDIT_NAME, POST_TITLE, text='testestest')
        d['post_id'] = post.id
        post.sticky()
        print("pvzbot needs to restart at this time...")

    xboneList = []
    ps4List = []
    originList = []

    post = r.get_submission(submission_id=d['post_id'])

    while True:
        post = r.get_submission(submission_id=d['post_id'])
        comments = post.comments
        for comment in comments:
            if comment.body[:5] == "[XBO]" and comment.id not in already_done:
                xboneList.append(str(comment.body)[6:] + " | /u/" + str(comment.author))
            if comment.body[:5] == "[PS$]" and comment.id not in already_done:
                ps4List.append(str(comment.body)[6:] + " | /u/" + str(comment.author))
            if comment.body[:8] == "[ORIGIN]" and comment.id not in already_done:
                originList.append(str(comment.body)[9:] + " | /u/" + str(comment.author))
            already_done.append(comment.id)

        xboneListCleaned = "##Xbox One\n\n"
        ps4ListCleaned = "##Playstation 4\n\n"
        originListCleaned = "##Origin (PC)\n\n"

        for item in xboneList:
            xboneListCleaned += "* " + item + "\n"
        for item in ps4List:
            ps4ListCleaned += "* " + item + "\n"
        for item in originList:
            originListCleaned += "* " + item + "\n"

        new_body = POST_HEADER + "\n" + xboneListCleaned + "\n" + ps4ListCleaned + "\n" + originListCleaned
        post.edit(new_body)
        currentTime = '[' + str(datetime.now().strftime("%H:%M:%S")) + '] '
        print(currentTime + "Sleeping for " + str(WAIT_TIME) +  " seconds.")
        time.sleep(WAIT_TIME)

if __name__ == "__main__":
	main()
