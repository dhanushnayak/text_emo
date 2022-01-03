import os
import warnings
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import neattext.functions as nt
#from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer,TfidfVectorizer
from sklearn.metrics import f1_score,accuracy_score,classification_report
from sklearn.ensemble import RandomForestClassifier
import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def eval_metrics(actual, pred):
    acc = accuracy_score(actual,pred)
    f1= f1_score(actual, pred, average='micro')
    report = classification_report(actual,pred)
    #rmse = np.sqrt(mean_squared_error(actual, pred))
    #mae = mean_absolute_error(actual, pred)
    #r2 = r2_score(actual, pred)
    return acc, f1,report


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    # Read the wine-quality csv file from the URL
    csv_url =  "https://raw.githubusercontent.com/Jcharis/end2end-nlp-project/main/notebooks/data/emotion_dataset_raw.csv"
    try:
        data = pd.read_csv(csv_url)
    except Exception as e:
        logger.exception(
            "Unable to download training & test CSV, check your internet connection. Error: %s", e
        )
    data['clear_text']=data['Text'].apply(nt.remove_stopwords).apply(nt.remove_userhandles)
    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data,test_size=0.3)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train['clear_text']
    test_x = test['clear_text']
    train_y = train['Emotion']
    test_y = test["Emotion"]

    c = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    #l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    with mlflow.start_run():
        rf =  Pipeline([('cv',TfidfVectorizer(ngram_range=(1,4),min_df=1)),('rf',RandomForestClassifier(n_estimators=int(c)))])
        rf.fit(train_x, train_y)

        predicted_qualities = rf.predict(test_x)

        (acc, f1,report) = eval_metrics(test_y, predicted_qualities)

        print("RF model (n_estimators=%f):" % (c))
        print("  ACC: %s" % acc)
        print("  F1: %s" % f1)
        print("  Report: %s" % report)

        mlflow.log_param("n_estimator", c)
        #mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("acc", acc)
        mlflow.log_metric("f1", f1)
        #mlflow.log_metric("report", report)
        

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        # Model registry does not work with file store
        if tracking_url_type_store != "file":

            # Register the model
            # There are other ways to use the Model Registry, which depends on the use case,
            # please refer to the doc for more information:
            # https://mlflow.org/docs/latest/model-registry.html#api-workflow
            mlflow.sklearn.log_model(rf, "model_rf", registered_model_name="RandomForestTextModel")
        else:
            mlflow.sklearn.log_model(rf, "model_rf")