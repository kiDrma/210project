import sqlite3
import random
import datetime
import csv

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
        Date_Posted DATE
    )
"""

cursor.execute(create_table)

database_size = 1000
id = 0
text = ""
sentiment = ""
keyword = ""
reason = ""
platform = ""
date = datetime.date.today()
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
            INSERT INTO posts(PostID, Post_Text, Sentiment, Keyword, Reason, Platform, Date_Posted)
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
    print(rand_sent)
    if platform == "Twitter":
        if rand_sent < .70:
            sentiment = "Positive"
        else:
            sentiment = "Negative"
    elif platform == "Instagram":
        if rand_sent < .60:
            sentiment = "Negative"
        else:
            sentiment = "Positive"
    else:
        if rand_sent <.50:
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

def random_date():
    global date
    year = random.randint(2019, 2024)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    
    date = datetime.date(year, month, day)

def make_random_post():
    global id
    random_post_platform_sentiment()
    random_post_reason_keyword()
    random_text()
    random_date()

    id = id + 1
    return [id, text, sentiment, keyword, reason, platform, date]

def export_to_csv():
    cursor.execute("SELECT * FROM Posts")
    rows = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    # Write to CSV file
    with open('posts_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)  # Write the header
        writer.writerows(rows)  # Write the data rows

    print("Data has been successfully written to posts_data.csv.")

def main():
    generate_data()
    export_to_csv()
    conn.close()

if __name__ == "__main__":
    main()

