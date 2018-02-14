import pandas as pd
import json
import sys

if "config.json":
    with open("config.json", "r") as f:
        config = json.load(f)

if "postData.txt":

    with open("postData.txt", encoding = "utf8") as f:
        answers = []
        reader = pd.read_csv(f, delimiter = config["Delimiter"], encoding = 'utf8')
        i = 0
        while i < len(reader['answer']):
            answers.append(reader['answer'][i])
            i += 1
        testingPairs = round(len(reader['question']), ndigits=5)



        with open('train.from', 'a', encoding='utf8') as f:
            for question in reader['question'][testingPairs:]:
                f.write(repr(question) + '\n')
        with open('train.to', 'a', encoding='utf8') as f:
            for answer in answers[testingPairs:]:
                f.write(repr(answer) + '\n')
        with open('test.from', 'a', encoding='utf8') as f:
            for question in reader['question'][:testingPairs]:
                f.write(repr(question) + '\n')
        with open('test.to', 'a', encoding='utf8') as f:
            for answer in answers[:testingPairs]:
                f.write(repr(answer) + '\n')
