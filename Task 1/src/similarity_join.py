import re
import pandas as pd
import numpy as np
class SimilarityJoin:
    def __init__(self, data_file1, data_file2):
        self.df1 = pd.read_csv(data_file1)
        self.df2 = pd.read_csv(data_file2)

    def preprocess_df(self, df, cols): 
        df = df.fillna('')
        df['joinkey'] = df.iloc[:, 1].map(str) + ' ' + df.iloc[:, 3]
        
        to_lower = lambda x: x.lower() #function to convert to lowercase
        tokenizer = lambda x: re.split(r'\W+', x) #funtion to generate tokens
        df['joinkey'] = df['joinkey'].apply(to_lower).apply(tokenizer)
        return df        

    def filtering(self, df1, df2):
        #exploding the 'joinkey' column
        def seperate(df): 
            df.reset_index(inplace=True)
            rows = []
            _ = df.apply(lambda row: [rows.append([row['id'], row['joinkey'], jk]) 
                                     for jk in row.joinkey], axis=1)
            df_new = pd.DataFrame(rows, columns=df.columns)
            return df_new
        
        df1 = df1.filter(['id','joinkey'], axis=1)
        df2 = df2.filter(['id','joinkey'], axis=1)
        seperate_df1 = seperate(df1).rename(columns={'index': 'id1', 'id': 'joinKey1', 'joinkey': 'jk1'}) #explode df1
        seperate_df2 = seperate(df2).rename(columns={'index': 'id2', 'id': 'joinKey2', 'joinkey': 'jk2'}) #explode df2
        seperate_df1 = seperate_df1.drop(seperate_df1[seperate_df1.jk1 == ''].index)
        seperate_df2 = seperate_df2.drop(seperate_df2[seperate_df2.jk2 == ''].index)
        
        cand_df = pd.merge(seperate_df1, seperate_df2, left_on='jk1', right_on='jk2') #join based on same joinkeys
        cand_df = cand_df.drop_duplicates(subset=['id1', 'id2'], keep='last') #dropping duplicates
        return cand_df
        
    def verification(self, cand_df, threshold):
        #calculating jaccard similarly 
        def jaccard_sim(row):
            set1 = set(row[1])
            set2 = set(row[4])
            jac = len(set1.intersection(set2)) / len(set1.union(set2))
            return jac
        
        cand_df['jaccard'] = cand_df.apply(jaccard_sim, axis=1) #appending jaccard similarity as a column
        result_df = cand_df.drop(cand_df[cand_df.jaccard < threshold].index) #dropping the entries below threshold
        return result_df

    def evaluate(self, result, ground_truth):
        result = set(map(tuple, result))
        ground_truth = set(map(tuple, ground_truth))
        tp = tuple(set(result).intersection(set(ground_truth)))
        
        precision = len(tp)/len(result)
        recall = len(tp)/len(ground_truth) 
        f_measure = (2 * precision * recall) / (precision + recall)
        return precision, recall, f_measure
    

    def jaccard_join(self, cols1, cols2, threshold):
        new_df1 = self.preprocess_df(self.df1, cols1)
        new_df2 = self.preprocess_df(self.df2, cols2)
        print ("Before filtering: %d pairs in total" %(self.df1.shape[0] *self.df2.shape[0])) 
        
        cand_df = self.filtering(new_df1, new_df2)
        print ("After Filtering: %d pairs left" %(cand_df.shape[0]))

        result_df = self.verification(cand_df, threshold)
        print ("After Verification: %d similar pairs" %(result_df.shape[0]))

        return result_df



if __name__ == "__main__":
    er = SimilarityJoin("Amazon_sample.csv", "Google_sample.csv")
    amazon_cols = ["title", "manufacturer"]
    google_cols = ["name", "manufacturer"]
    result_df = er.jaccard_join(amazon_cols, google_cols, 0.5)

    result = result_df[['id1', 'id2']].values.tolist()
    ground_truth = pd.read_csv("Amazon_Google_perfectMapping_sample.csv").values.tolist()
    print ("(precision, recall, fmeasure) = ", er.evaluate(result, ground_truth))