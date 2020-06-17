from pandas import DataFrame
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from word_to_vec import *
from preprocess import *
import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score
import joblib


def get_train_data(spamDir, hamDir, val=None):
    allDir = []
    allDir.append(spamDir)
    allDir.append(hamDir)
    if val is None:
        model = build_train_word2vec(allDir)
    spam_fea = create_feature(spamDir)
    ham_fea = create_feature(hamDir)

    #ham_email = DataFrame(ham_fea)
    #spam_email = DataFrame(spam_fea)

    columns = ['html', 'javascript', 'urlCount', 'attachCount']
    for i in range(100):
        columns.append('vector{}'.format(i))

    ham_email = DataFrame(ham_fea, columns=columns)
    spam_email = DataFrame(spam_fea, columns=columns)
    train_x = pd.concat([spam_email, ham_email], axis=0)
    train_x = train_x.reset_index()
    ham_email['label'] = 0
    spam_email['label'] = 1
    train_y = pd.concat([spam_email['label'], ham_email['label']], axis=0)
    train_y = train_y.reset_index()
    #x_train, x_test, y_train, y_test = train_test_split(train_x, train_y, random_state=42)
    x_train = train_x.drop(['index'], axis=1)
    #x_test = x_test.drop(['index'], axis=1)
    y_train = train_y.drop(['index'], axis=1)
    #y_test = y_test.drop(['index'], axis=1)
    return x_train, y_train


if __name__ == '__main__':
    x_test, y_test = get_train_data('/Users/hujie/Desktop/corpus/spam', '/Users/hujie/Desktop/corpus/ham', val=1)
    #xgb = XGBClassifier(n_estimators=500)
    #xgb.fit(x_train, y_train)
    xgb = joblib.load('xgb')
    #joblib.dump(xgb, 'xgb')
    preds = xgb.predict(x_test)
    print('accu:{:.3f}'.format(accuracy_score(y_test, preds)))
    print('f1_score:{:.3f}'.format(f1_score(y_test, preds)))
    #x_train.to_csv('/Users/hujie/Desktop/x_train.csv', index=False)
    #y_train.to_csv('/Users/hujie/Desktop/temp_data/y_train.csv', index=False)
    #x_test.to_csv('/Users/hujie/Desktop/temp_data/x_test.csv', index=False)
    #y_test.to_csv('/Users/hujie/Desktop/temp_data/y_test.csv', index=False)
