import csv
import urllib.request
import json
from tqdm import tqdm

from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax

# Tasks:
# emoji, emotion, hate, irony, offensive, sentiment
# stance/abortion, stance/atheism, stance/climate, stance/feminist, stance/hillary

TASK = "sentiment"
MODEL = f"cardiffnlp/twitter-roberta-base-{TASK}"

tokenizer = AutoTokenizer.from_pretrained(MODEL)

# download label mapping
labels = []
mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{TASK}/mapping.txt"
with urllib.request.urlopen(mapping_link) as f:
    html = f.read().decode("utf-8").split("\n")
    csvreader = csv.reader(html, delimiter="\t")
labels = [row[1] for row in csvreader if len(row) > 1]

# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
model.save_pretrained(MODEL)


# Initialize sentiment counters
positive = 0
neutral = 0
negative = 0

# Read the JSON file with the list of comments
with open("comments.json", mode="r", encoding="utf-8") as file:
    list_of_comments = json.loads(file.read())

# Filter comments with more than 500 characters because the
# has a limit of 524 characters
list_of_comments = [c for c in list_of_comments if len(c) < 500]

# Run the inference for every comment
for comment in tqdm(list_of_comments):
    encoded_input = tokenizer(comment, return_tensors="pt")
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    for i in range(scores.shape[0]):
        l = labels[ranking[i]]
        s = scores[ranking[i]]
        if l == "positive":
            positive += 1
            break
        if l == "neutral":
            neutral += 1
            break
        negative += 1


print([positive, neutral, negative])
