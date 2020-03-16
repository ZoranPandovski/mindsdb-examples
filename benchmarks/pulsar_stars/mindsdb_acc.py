import mindsdb
import sys
import pandas as pd
from sklearn.metrics import balanced_accuracy_score


def run(sample):
    backend='lightwood'

    mdb = mindsdb.Predictor(name='pulsar_star_model')

    mdb.learn(from_data='dataset/train.csv', to_predict='target_class', backend=backend, stop_training_in_x_seconds=10)

    test_df = pd.read_csv('dataset/test.csv')
    predictions = mdb.predict(when_data='dataset/test.csv')

    results = [x['target_class'] for x in predictions]
    real = list(test_df['target_class'])

    accuracy = balanced_accuracy_score(list(map(int,real)), list(map(int,results)))
    print(f'Balacned accuracy score of {accuracy}')

    return {
        'accuracy': accuracy
        ,'accuracy_function': 'balanced_accuracy_score'
        ,'backend': backend
    }

if __name__ == '__main__':
    sample = bool(sys.argv[1]) if len(sys.argv) > 1 else False
    result = run(sample)
    print(result)
