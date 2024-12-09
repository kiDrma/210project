import sqlite3
import random
import csv

# Edit database features before generation
database_size = 10000
percent_twitternegative = 0.30 
percent_instanegative = 0.65
percent_facebooknegative = 0.5
start_year = 2016
end_year = 2024
pos_increase = 0.1 # Between 0 and 1

random.seed(123)

conn = sqlite3.connect("posts.db")
cursor = conn.cursor()

# Create table
create_table = """
    CREATE TABLE IF NOT EXISTS Posts(
        PostID INT PRIMARY KEY,
        Post_Text VARCHAR(500),
        Sentiment VARCHAR(30),
        Keyword VARCHAR(30),
        Reason VARCHAR(30),
        Platform VARCHAR(30),
        Year INT
    )
"""

cursor.execute(create_table)

id = 0
text = ""
sentiment = ""
keyword = ""
reason = ""
platform = ""
year = 0
negative_keywords = ["bad", "horrible", "disastrous", "terrifying", "scary", "unethical", "concerning"]
positive_keywords = ["innovative", "productive", "amazing", "beneficial", "hopeful", "good", "great"]
posreason_keywords = ["helpful", "useful", "productive", "automation", "learning"]
negreason_keywords = ["jobs", "bias", "inhuman", "environment", "creativity"]
filler_words = ["is", "a", "the", "I", "think", "this", "that", "it", "might", "could", "be", "very", "most", "use", "to", "on", "by", "from", "with", "well", "believe", "beliefs", "not"]

# Function to insert random data into the database
def generate_data():
    for i in range(database_size):
        new_post = make_random_post()
        cursor.execute("""
            INSERT INTO posts(PostID, Post_Text, Sentiment, Keyword, Reason, Platform, Year)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, new_post)
        
    conn.commit()

# Generates random platform + sentiment
def random_post_platform_sentiment():
    global platform
    global sentiment
    random_platform = random.randint(0, 2)
    if random_platform == 0:
        platform = "Twitter"
    elif random_platform == 1:
        platform = "Instagram"
    else:
        platform = "Facebook"

    rand_sent = random.random()
    year_increase = abs(start_year - year) * pos_increase / (end_year - start_year)
    rand_sent = rand_sent + year_increase
    if platform == "Twitter":
        if rand_sent < percent_twitternegative:
            sentiment = "Negative"
        else:
            sentiment = "Positive"
    elif platform == "Instagram":
        if rand_sent < percent_instanegative:
            sentiment = "Negative"
        else:
            sentiment = "Positive"
    else:
        if rand_sent < percent_facebooknegative:
            sentiment = "Negative"
        else:
            sentiment = "Positive"

def random_post_reason_keyword():
    global reason
    global keyword
    if sentiment == "Negative":
        keyword = negative_keywords[random.randint(0, len(negative_keywords) - 1)]
        reason = negreason_keywords[random.randint(0, len(negreason_keywords) - 1)]
    else:
        keyword = positive_keywords[random.randint(0, len(positive_keywords) - 1)]
        reason = posreason_keywords[random.randint(0, len(posreason_keywords) - 1)]

def random_text():
    global text
    words_to_include = [keyword, reason]
    random_words = random.choices(filler_words, k = 10)

    text = " ".join(words_to_include + random_words)

def random_year():
    global year
    year = random.randint(start_year, end_year)
    
def make_random_post():
    global id
    random_year()
    random_post_platform_sentiment()
    random_post_reason_keyword()
    random_text()

    id = id + 1
    return [id, text, sentiment, keyword, reason, platform, year]

def export_to_csv():
    cursor.execute("SELECT * FROM Posts")
    rows = cursor.fetchall()

    column_names = [description[0] for description in cursor.description]

    with open('posts_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)
        writer.writerows(rows)  

def main():
    generate_data()
    export_to_csv()
    conn.close()

if __name__ == "__main__":
    main()

