from pickle import TRUE
import tweepy
import WebQueries
import mysql.connector

KEYS_FILE = "/home/molefi/Documents/negligible/keys.txt"
DB ="/home/molefi/Documents/negligible/LocalDataBase.txt" 

AllKeys = open(KEYS_FILE, "r").read().splitlines()
APIkey = AllKeys[1]
APISecretKey = AllKeys[3]
BearerToken = AllKeys[5]
AccessToken = AllKeys[7]
SecretAccessToken = AllKeys[9]
QUERY_CLIENT = tweepy.Client(bearer_token= BearerToken)
TWEET_CLIENT = tweepy.Client(consumer_key= APIkey,
    consumer_secret= APISecretKey,
    access_token= AccessToken,
    access_token_secret= SecretAccessToken)

DB_credentials = open(DB, "r").read().splitlines()
DB_connection = mysql.connector.connect(
    user = DB_credentials[3], 
    database = DB_credentials[1], 
    password = DB_credentials[7]
    )


def main():
    # use one buffered  cursor throughout?
    TweetTableCursor= DB_connection.cursor(buffered= True) 
    WordOfDayCursor = DB_connection.cursor(buffered= True, dictionary= True)
    
    words_location = eval(input("run get_word?"))
    if words_location == True:
        get_word()

    WordOfDayCursor.execute("SELECT * FROM HistoricalWords")

    recent_tweets_run = eval(input("run tweet request?"))
    if recent_tweets_run == True:
        for row in WordOfDayCursor:
            query= request_recenttweets(QUERY_CLIENT, row['Site'], row['Word'])
            TweetTableCursor.executemany("INSERT INTO StoredTweets"
                                "(ids, Tweet, WordOfDay, Site, Retweet)" 
                                "VALUES(%s, %s, %s, %s, %s)", 
                                query)
            DB_connection.commit()

    TweetTableCursor.execute("SELECT * FROM StoredTweets WHERE Retweet = 0")
    
    for row in TweetTableCursor:
        TWEET_CLIENT.retweet(tweet_id = row[0], 
        user_auth = True)
        WordOfDayCursor.execute(
            "UPDATE StoredTweets SET Retweet = 1 WHERE ids = %s", 
            [row[0]]
        )
        DB_connection.commit()
    
    

def get_word():
    DBcursor= DB_connection.cursor(buffered= True)

    dictionary_word= WebQueries.dic_query()
    webster_word= WebQueries.merriam_webster_query()
    urban_word= WebQueries.ub_query()

    
    word_list= {"Dictionary.com":dictionary_word, 
    "merriam-webster.com": webster_word, 
    "urbandictionary.com": urban_word }
    
    for keys in word_list:
        DBcursor.execute("INSERT INTO HistoricalWords"
                        "(Word, Site)"
                        "VALUES(%s, %s)", (word_list[keys], keys))
    DB_connection.commit()

def request_recenttweets(client, site, word_of_day):
    DB_query_setup= []
      
    try:
        twitter_payload = client.search_recent_tweets(query= word_of_day, max_results = 10)

    except:
        
        print(f"an error occured, the query is {word_of_day}")
        choice = eval(input("want to break?:"))
        if choice == True:
            pass       
    
    try:
        for tweet in twitter_payload.data:
            tweetID = tweet.data['id']
            tweettext = tweet.data['text']
            DB_query_setup.append((int(tweetID), tweettext, word_of_day, site, 0))
            
    except:
        
        print(f"an error occured, the word is {word_of_day} and the tweet text: '\n' {site}")
        choice = eval(input("want to pass?:"))
        if choice == True:
            pass
    
    return DB_query_setup


if __name__ ==  "__main__":
    main()
