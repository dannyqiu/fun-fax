class DummySearch:

    def search(self, query):
        results = [
            {
                "type": "submission",
                "title": "Fun fact: Did you know that you inputted {} into the search box?".format(query),
                "subreddit": "fun-fax-testing",
                "permalink": "/",
                "score": 999999,
            },
            {
                "type": "submission",
                "title": "Fun fact about the Vatican",
                "subreddit": "funny",
                "permalink": "https://reddit.com/r/funny/comments/16z5sr/fun_fact_about_the_vatican/",
                "score": 0.999,
            },
            {
                "type": "submission",
                "title": "TIL Corey Feldman already made a movie about killing Bin Laden",
                "subreddit": "todayilearned",
                "permalink": "https://reddit.com/r/todayilearned/comments/h2l9w/til_corey_feldman_already_made_a_movie_about/",
                "score": 0.459,
            },
            {
                "type": "comment",
                "title": "Shaq hit almost 12,000 baskets in his career. Exactly 1 of them was a 3-pointer.",
                "subreddit": "askreddit",
                "permalink": "https://www.reddit.com/r/AskReddit/comments/4lmm61/what_is_a_fun_fact_that_always_blows_peoples_minds/d3os740/",
                "score": 0.589,
            },
            {
                "type": "submission",
                "title": "YSK Useful Tips For A Rainy Day",
                "subreddit": "YouShouldKnow",
                "permalink": "https://reddit.com/r/YouShouldKnow/comments/16zf8g/ysk_useful_tips_for_a_rainy_day/",
                "score": 0.123,
            },
        ]
        return results
