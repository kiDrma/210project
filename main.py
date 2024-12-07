import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("posts.db")
cursor = conn.cursor()

# Find % of how many POSITIVE posts came from which platforms
cursor.execute("SELECT COUNT (*) FROM Posts WHERE Platform = 'Twitter'")
total_twitter = cursor.fetchone()[0]

cursor.execute("SELECT COUNT (*) FROM Posts WHERE Platform = 'Instagram'")
total_insta = cursor.fetchone()[0]

cursor.execute("SELECT COUNT (*) FROM Posts WHERE Platform = 'Facebook'")
total_facebook = cursor.fetchone()[0]

print(total_insta)
print(total_twitter)
print(total_facebook)

cursor.execute("SELECT COUNT (*) FROM Posts WHERE Sentiment = 'Positive'")
total_pos = cursor.fetchone()[0]

cursor.execute("SELECT COUNT (*) FROM Posts WHERE Platform = 'Instagram' AND Sentiment = 'Positive'")
pos_insta = cursor.fetchone()[0]

cursor.execute("SELECT COUNT (*) FROM Posts WHERE Platform = 'Twitter' AND Sentiment = 'Positive'")
pos_twitter = cursor.fetchone()[0]

cursor.execute("SELECT COUNT (*) FROM Posts WHERE Platform = 'Facebook' AND Sentiment = 'Positive'")
pos_facebook = cursor.fetchone()[0]

print(pos_insta / total_pos * 100)
print(pos_twitter / total_pos * 100)
print(pos_facebook / total_pos * 100)


# Find % of how many NEGATIVE posts came from which platforms
cursor.execute("SELECT COUNT (*) FROM Posts WHERE Sentiment = 'Negative'")
total_neg = cursor.fetchone()[0]

cursor.execute("SELECT COUNT (*) FROM Posts WHERE Platform = 'Instagram' AND Sentiment = 'Negative'")
neg_insta = cursor.fetchone()[0]

cursor.execute("SELECT COUNT (*) FROM Posts WHERE Platform = 'Twitter' AND Sentiment = 'Negative'")
neg_twitter = cursor.fetchone()[0]

cursor.execute("SELECT COUNT (*) FROM Posts WHERE Platform = 'Facebook' AND Sentiment = 'Negative'")
neg_facebook = cursor.fetchone()[0]

print(neg_insta / total_neg * 100)
print(neg_twitter / total_neg * 100)
print(neg_facebook / total_neg * 100)

# Plot negative sentiment by platform
cursor.execute("SELECT Platform, COUNT (*) FROM Posts WHERE Sentiment = 'Negative' GROUP BY Platform")
neg_bardata = cursor.fetchall()

neg_platforms = [row[0] for row in neg_bardata]
neg_counts = [row[1] for row in neg_bardata]

plt.figure()
plt.bar(neg_platforms, neg_counts, color=['navy', 'mediumvioletred', 'turquoise']) 
plt.title('Number of Negative Posts by Platform')
plt.xlabel('Platform')
plt.ylabel('Number of Negative Posts')
#plt.show()

# Plot positive sentiment by platform
cursor.execute("SELECT Platform, COUNT (*) FROM Posts WHERE Sentiment = 'Positive' GROUP BY Platform")
pos_bardata = cursor.fetchall()

pos_platforms = [row[0] for row in pos_bardata]
pos_counts = [row[1] for row in pos_bardata]

plt.figure()
plt.bar(pos_platforms, pos_counts, color=['navy', 'mediumvioletred', 'turquoise']) 
plt.title('Number of Positive Posts by Platform')
plt.xlabel('Platform')
plt.ylabel('Number of Positive Posts')
plt.show()

# Plot sentiments for Twitter
cursor.execute("SELECT Sentiment, COUNT (*) FROM Posts WHERE Platform = 'Twitter' GROUP BY Sentiment")
twittersent_bardata = cursor.fetchall()

twittersent_platforms = [row[0] for row in twittersent_bardata]
twittersent_counts = [row[1] for row in twittersent_bardata]

plt.figure()
plt.bar(twittersent_platforms, twittersent_counts, color=['red', 'green']) 
plt.title('Twitter Sentiments')
plt.xlabel('Sentiment')
plt.ylabel('Number of Posts')
plt.show()

# Plot sentiments for Instagram
cursor.execute("SELECT Sentiment, COUNT (*) FROM Posts WHERE Platform = 'Instagram' GROUP BY Sentiment")
instasent_bardata = cursor.fetchall()

instasent_platforms = [row[0] for row in instasent_bardata]
instasent_counts = [row[1] for row in instasent_bardata]

plt.figure()
plt.bar(instasent_platforms, instasent_counts, color=['red', 'green']) 
plt.title('Instagram Sentiments')
plt.xlabel('Sentiment')
plt.ylabel('Number of Posts')
plt.show()

# Plot sentiments for Facebook
cursor.execute("SELECT Sentiment, COUNT (*) FROM Posts WHERE Platform = 'Facebook' GROUP BY Sentiment")
facebooksent_bardata = cursor.fetchall()

facebooksent_platforms = [row[0] for row in facebooksent_bardata]
facebooksent_counts = [row[1] for row in facebooksent_bardata]

plt.figure()
plt.bar(facebooksent_platforms, facebooksent_counts, color=['red', 'green']) 
plt.title('Facebook Sentiments')
plt.xlabel('Sentiment')
plt.ylabel('Number of Posts')
plt.show()

# Plot overall sentiments
cursor.execute("SELECT Sentiment, COUNT (*) FROM Posts GROUP BY Sentiment")
sentiment_bardata = cursor.fetchall()

sent_platforms = [row[0] for row in sentiment_bardata]
sent_counts = [row[1] for row in sentiment_bardata]

plt.figure()
plt.bar(sent_platforms, sent_counts, color=['red', 'green']) 
plt.title('Overall Sentiments')
plt.xlabel('Sentiment')
plt.ylabel('Number of Posts')
plt.show()


#plt.savefig('negative_by_platform.png') 
#plt.close()

conn.close()