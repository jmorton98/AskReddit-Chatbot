import praw
import json
import sys
import csv
import time
import smtplib
import pandas as pd


if "config.json":
    with open("config.json", "r") as f:
        config = json.load(f)
else:
    print("config file not in directory")
    sys.exit()


login = praw.Reddit(client_id = config["RedditInfo"]["client_id"],
                     client_secret = config["RedditInfo"]["client_secret"],
                     username = config["RedditInfo"]["username"],
                     password = config["RedditInfo"]["password"],
                     user_agent = config["RedditInfo"]["user_agent"])


postsAlreadySeen = []
i = config["BatchSize"]


def topRedditposts(_subreddit):
    hotPosts = _subreddit.hot(limit = i)
    postIDs = []
    for submission in hotPosts:
        if submission not in postsAlreadySeen:
            postIDs.append(submission.id)
    for postID in postIDs:
        postsAlreadySeen.append(postID)
    return postIDs

def getTopComment(reddit, postID):
    comments = []
    titles = []
    if len(postID) > 0:
        for _id in postID:
            submission = reddit.submission(id = _id)
            if len(submission.comments) > 0:
                if submission.comments[0].body != "[removed]" and submission.comments[0].body != "[deleted]" and "[Serious]" not in submission.title and "](" not in submission.comments[0].body:
                    comment = ''.join(submission.comments[0].body.strip())
                    comment = comment.split('\n\n')
                    comment = " ".join(comment)
                    comments.append(comment.strip())
                    title = ''.join(submission.title)
                    titles.append(title)
                    print(title)
    return comments, titles

def bot(reddit):
    subreddit = reddit.subreddit(config["RedditInfo"]["TargetSubreddit"])
    comments, titles = getTopComment(login, topRedditposts(subreddit))
    print("retrieved comments and titles")
    collection = list(zip(titles, comments))
    if len(titles) > 0:
        with open("postData.txt", "a", encoding = 'utf-8') as f:
            csv_writer = csv.writer(f, delimiter = config["Delimiter"], lineterminator = '\n')
            csv_writer.writerows(collection)
    time.sleep(config["TimeToRefresh"])


KeepGoing = True

while KeepGoing:
    bot(login)
    if len(postsAlreadySeen) >= config["TotalSavedPairs"]:
        with open("postData.txt", encoding = "utf8") as f:
            reader = pd.read_csv(f, delimiter = config["Delimiter"], encoding = 'utf8')
            print(len(reader["question"]))
            if len(reader["question"]) >= config["TotalSavedPairs"]:

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.ehlo()
                server.starttls()

                server.login(config["EmailInfo"]["Sender"]["Email"], config["EmailInfo"]["Sender"]["Password"])

                msg = "\nYour bot has successfully collected your minimum amount of data requested for your reddit chatbot."
                server.sendmail(config["EmailInfo"]["Sender"]["Email"], config["EmailInfo"]["ReceivingEmail"], msg)

                server.close()

                KeepGoing = False
