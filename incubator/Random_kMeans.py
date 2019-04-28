class WeightedEmbeddingSearch:

    def __init__(self):
        #print("Loading data csv")
        #fun_fact_title_data = pd.read_csv(FUN_FACT_TITLE_CSV).dropna(subset=REQUIRED_COLUMNS)
        til_title_data = pd.read_csv(TIL_TITLE_CSV).dropna(subset=REQUIRED_COLUMNS)
        #ysk_title_data = pd.read_csv(YSK_TITLE_CSV).dropna(subset=REQUIRED_COLUMNS)

        self.title_data = pd.concat([
            #fun_fact_title_data,
            til_title_data,
            #ysk_title_data,
        ], join='inner').reset_index(drop=True)

        #print("Computing tf-idf matrix")
        self.vectorizer = TfidfVectorizer(stop_words='english', dtype=np.float32)
        tfidf_matrix = self.vectorizer.fit_transform(self.title_data["title"])

        #print("Loading spacy")
        self.nlp = spacy.load('en_core_web_lg')

        #print("Computing weighted embeddings")
        features = self.vectorizer.get_feature_names()
        self.f_vectors = np.array([self.nlp.vocab[f].vector for f in features])
        weighted_embeddings = tfidf_matrix.dot(self.f_vectors)
        assert weighted_embeddings.shape == (len(self.title_data.index), 300)
        self.n_weighted_embeddings = weighted_embeddings / (np.linalg.norm(weighted_embeddings, axis=1)[:, np.newaxis] + EPS)

        #print("Compressing pandas dataframe into index")
        #self.index = list(title_data.itertuples())

        #print("Done loading {} rows".format(len(self.title_data.index)))
    def random(self,method = 'similarity', top = 10):
        funfact = self.title_data.iloc[random.randint(0, len(self.title_data))]["title"]
        #print ("fact: " + funfact)
        #results = self.search(funfact, method, top)
        tokens = self.vectorizer.build_analyzer()(funfact)
        query_tok = [x for x in tokens if random.random() < .5]
        rand_query = " ".join(query_tok)
        #print ("rand: " + rand_query)
        return self.search(rand_query, method, top)
    
#     def query(self, query, method = 'similarity', top = 10):
#         return self.search(query, method, top)
    
    def search(self, query, method = 'similarity', top=10):
        query_tfidf = self.vectorizer.transform([query])
        if query_tfidf.count_nonzero() > 0:
            query_weighted = query_tfidf.dot(self.f_vectors).flatten()
        # average word embeddings if query words don't exist in our corpus (tfidf matrix)
        else:
            tokens = self.vectorizer.build_analyzer()(query)
            # query was all stopwords, so we'll have to manually tokenize
            if not tokens:
                tokens = query.lower().split()
            query_weighted = np.average([self.nlp.vocab[t].vector for t in tokens], axis=0).flatten()

        # if we have no embeddings for the given query, we're out of luck
        if np.count_nonzero(query_weighted) == 0:
            return []

        n_query_weighted = query_weighted / (np.linalg.norm(query_weighted) + EPS)
        rankings = self.n_weighted_embeddings.dot(n_query_weighted)
        rankings_index = np.argsort(-rankings)
        ranked_df = self.title_data.loc[rankings_index]
        ranked_titles = list(ranked_df['title'])
        ranked_scores = list(ranked_df['score'])
        top_ranked_em = self.n_weighted_embeddings[rankings_index]
        ranked_rankings = rankings[rankings_index]
        #print('about to call kmeans')
        results = self.kMeans(ranked_titles, ranked_scores, ranked_rankings, top_ranked_em, method)
        
#         index = list(ranked_df.itertuples())
        #print('done with itertuple')
        results = [
            {
                "type": "submission",
                "title": ranked_df.iloc[d]["title"],
                "subreddit": ranked_df.iloc[d]['subreddit'],
                "permalink": ranked_df.iloc[d]['permalink'],
                "score": ranked_df.iloc[d]['score']
            }
            for d in [i[1][0] for i in results]
        ]
        return results


    def kMeans(self, titles, scores, rankings, embeddings, method):
        TOP_HITS_KMEANS = max(40,np.sum(scipy.stats.zscore(rankings) > 3.5))
        if TOP_HITS_KMEANS > 200:
            TOP_HITS_KMEANS = 200
        kmeans = KMeans(n_clusters=20, random_state=0).fit(embeddings[:TOP_HITS_KMEANS])
        
        counter = collections.Counter(kmeans.labels_)
        most_common = counter.most_common(10)
        most_common = set([i[0] for i in most_common])
        results = self.topSimOfEachCluster(kmeans.labels_, 10, most_common)
        self.topScoreOfEachCluster(results, 4, scores)
        results = self.topResultsSorted(results, rankings, scores, method)
        return results
        
        
    # cluster number to top num based on similarity
    def topSimOfEachCluster(self, cluster_labels, num, most_common):
        #print('topsimofeachcluster')
        res = {}
        clusters_included = set(most_common)
        for i, el in enumerate(cluster_labels):
            if el not in clusters_included:
                continue
            if el not in res:
                res[el] = [i]
            elif len(res[el]) < num:
                res[el].append(i) 
        return res 
    
    #takes topOfEachCluster and gets the top num by score
    def topScoreOfEachCluster(self, sim_results, num, scores):
        #print('topscoreofeachcluster')
        for key in sim_results:
            sim_results[key].sort(key=lambda x: scores[x], reverse = True)
            sim_results[key] = sim_results[key][:num]
            
    #sort results by method        
    def topResultsSorted(self, results, rankings, scores, method = 'similarity'):
        #print('topresultssorted')
        if method == 'similarity':
            for key in results:
                results[key].sort(key=lambda x: rankings[x], reverse = True) #sorts within a cluster
                sorted_results = sorted(results.items(), key=lambda x: rankings[x[1][0]], reverse = True) #sorts all clusters
        elif method == 'score':
            for key in results:
                results[key].sort(key=lambda x: scores[x], reverse = True)
                sorted_results = sorted(results.items(), key=lambda x: scores[x[1][0]], reverse = True)
        return sorted_results