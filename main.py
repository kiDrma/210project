import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

conn = sqlite3.connect("posts.db")
cursor = conn.cursor()

def summary():
    # Find % of how many POSITIVE posts came from which platforms
    cursor.execute("SELECT COUNT (*) FROM Posts WHERE Sentiment = 'Positive'")
    total_pos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT (*) FROM Posts WHERE Platform = 'Instagram' AND Sentiment = 'Positive'")
    pos_insta = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT (*) FROM Posts WHERE Platform = 'Twitter' AND Sentiment = 'Positive'")
    pos_twitter = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT (*) FROM Posts WHERE Platform = 'Facebook' AND Sentiment = 'Positive'")
    pos_facebook = cursor.fetchone()[0]

    # Find % of how many NEGATIVE posts came from which platforms
    cursor.execute("SELECT COUNT (*) FROM Posts WHERE Sentiment = 'Negative'")
    total_neg = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT (*) FROM Posts WHERE Platform = 'Instagram' AND Sentiment = 'Negative'")
    neg_insta = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT (*) FROM Posts WHERE Platform = 'Twitter' AND Sentiment = 'Negative'")
    neg_twitter = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT (*) FROM Posts WHERE Platform = 'Facebook' AND Sentiment = 'Negative'")
    neg_facebook = cursor.fetchone()[0]

    # Find most popular reasons for positive and negative sentiments
    cursor.execute("SELECT Reason, COUNT (*) FROM Posts WHERE Sentiment = 'Positive'")
    pos_reason = cursor.fetchall()

    cursor.execute("SELECT Reason, COUNT (*) FROM Posts WHERE Sentiment = 'Negative'")
    neg_reason = cursor.fetchall()

    with open('summary.txt', 'w') as file:
        file.write(f'% of positive posts that came from Instagram: {round(pos_insta / total_pos * 100, 2)}%\n')
        file.write(f'% of positive posts that came from Twitter: {round(pos_twitter / total_pos * 100, 2)}%\n')
        file.write(f'% of positive posts that came from Facebook: {round(pos_facebook / total_pos * 100, 2)}%\n')
        file.write(f'Total # of positive posts: {total_pos}\n\n')
        file.write(f'% of negative posts that came from Instagram: {round(neg_insta / total_neg * 100, 2)}%\n')
        file.write(f'% of negative posts that came from Twitter: {round(neg_twitter / total_neg * 100, 2)}%\n')
        file.write(f'% of negative posts that came from Facebook: {round(neg_facebook / total_neg * 100, 2)}%\n')
        file.write(f'Total # of negative posts: {total_neg}\n\n')
        file.write(f'Most popular reason for positive sentiments: {pos_reason[0][0]}\n')
        file.write(f'Most popular reason for negative sentiments: {neg_reason[0][0]}\n\n')



def plot_data():
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

    # Plot sentiments by year
    cursor.execute("SELECT Year, COUNT (*) FROM Posts WHERE Sentiment = 'Positive' GROUP BY Year ORDER BY Year")
    yearly_sentiments = cursor.fetchall()

    years = [row[0] for row in yearly_sentiments]
    positive_counts = [row[1] for row in yearly_sentiments]

    plt.figure()
    plt.plot(years, positive_counts, marker = 'o', color='black') 
    plt.title('Positive Sentiments By Year')
    plt.xlabel('Sentiment')
    plt.ylabel('Number of Posts')
    plt.show()

def predict_future():
    cursor.execute("SELECT Year, COUNT (*) FROM Posts WHERE Sentiment = 'Positive' GROUP BY Year ORDER BY Year")
    sentiment_by_year = cursor.fetchall()
    sentiment_by_year = pd.DataFrame(sentiment_by_year, columns=['Year', 'Positive_Sentiment'])

    x_values = sentiment_by_year[['Year']]
    y_values = sentiment_by_year[['Positive_Sentiment']]

    model = LinearRegression()
    model.fit(x_values, y_values)

    future_years = np.arange(sentiment_by_year['Year'].max() + 1, sentiment_by_year['Year'].max() + 6, 1)

    future_years_to_predict = pd.DataFrame({'Year': future_years})
    forecast = model.predict(future_years_to_predict)

    plt.scatter(x_values, y_values, label='Historical Data', color='blue')
    plt.plot(x_values, model.predict(x_values), label='Fitted Line', color='black')
    plt.plot(future_years_to_predict, forecast, label='Forecast', color='purple', marker='o')
    plt.xlabel('Year')
    plt.ylabel('Positive Sentiment')
    plt.legend()
    plt.title('Positive Sentiment Forecast')
    plt.show()


    cursor.execute("SELECT Year, COUNT (*) FROM Posts WHERE Sentiment = 'Negative' GROUP BY Year ORDER BY Year")
    negsentiment_by_year = cursor.fetchall()
    negsentiment_by_year = pd.DataFrame(negsentiment_by_year, columns=['Year', 'Negative_Sentiment'])

    negx_values = negsentiment_by_year[['Year']]
    negy_values = negsentiment_by_year[['Negative_Sentiment']]

    negmodel = LinearRegression()
    negmodel.fit(negx_values, negy_values)

    negforecast = negmodel.predict(future_years_to_predict)

    plt.scatter(negx_values, negy_values, label='Historical Data', color='blue')
    plt.plot(negx_values, negmodel.predict(negx_values), label='Fitted Line', color='black')
    plt.plot(future_years_to_predict, negforecast, label='Forecast', color='purple', marker='o')
    plt.xlabel('Year')
    plt.ylabel('Negative Sentiment')
    plt.legend()
    plt.title('Negative Sentiment Forecast')
    plt.show()

def main():
    #summary()
    #plot_data()
    #predict_future()
    conn.close()

if __name__ == "__main__":
    main()