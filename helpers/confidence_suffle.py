import random
import mindsdb
import numpy as np

'''
1. Get the normal accuracy & confidence
2. Get the accuracy & confidence with some missing columns
3. With a combination of all columns from step 2, get an accuracy & confidence

accuracy / confidence (1) > accuracy / confidence (2) > accuracy / confidence (3)

1. Get accuracy for all predctions
2. Get the top 50% of predictions based on the confidence
3. Get the accuracy for those 50%

accuracy (3) > accuracy(1)
'''


def confidence_suffle(columns, df_train, df_test, acc_score, to_predict):
    random.seed(2)
    confidences_missing_1 = []
    accurcy_missing_1 = []
    columns_missing_1 = []

    predictor = mindsdb.Predictor(name='confidence_test')
    predictor.learn(from_data=df_train, to_predict=to_predict, stop_training_in_x_seconds=10)
    predictions = predictor.predict(when_data=df_test)
    explainations = [x.explanation for x in predictions]

    normal_confidence = np.mean(np.array( [x[to_predict]['confidence'] for x in explainations] ))

    norma_accuracy = acc_score(list(df_test[to_predict]), [x[to_predict]['predicted_value'] for x in explainations])

    previously_removed = []
    for i in range(max(len(columns),2)):
        remove_columns = [random.choice(columns)]
        previously_removed.append(remove_columns[0])
        columns_missing_1.append(remove_columns)

        train = df_train.drop(columns=remove_columns)
        test = df_test.drop(columns=remove_columns)

        predictor = mindsdb.Predictor(name='confidence_test')
        predictor.learn(from_data=train, to_predict=to_predict, stop_training_in_x_seconds=10)
        predictions = predictor.predict(when_data=test)
        explainations = [x.explanation for x in predictions]

        confidences_missing_1.append(np.mean(np.array([x[to_predict]['confidence'] for x in explainations])))
        accurcy_missing_1.append(acc_score(list(test[to_predict]), [x[to_predict]['predicted_value'] for x in explainations]))

    train = df_train.drop(columns=previously_removed)
    test = df_test.drop(columns=previously_removed)

    predictor = mindsdb.Predictor(name='confidence_test')
    predictor.learn(from_data=train, to_predict=to_predict, stop_training_in_x_seconds=10)
    predictions = predictor.predict(when_data=test)
    explainations = [x.explanation for x in predictions]

    multiple_removed_confidence = np.mean(np.array([x[to_predict]['confidence'] for x in explainations]))
    multiple_removed_accuracy = acc_score(list(test[to_predict]), [x[to_predict]['predicted_value'] for x in explainations])

    for i in range(len(confidences_missing_1)):
        conf = confidences_missing_1[i]
        acc = accurcy_missing_1[i]
        missing = columns_missing_1[i]

        if conf >= normal_confidence:
            print(f'Got confidence of {conf} with missing columns {missing} which is bigger than the normal confidence {normal_confidence}')

        if conf <= multiple_removed_confidence:
            print(f'Got confidence of {conf} with missing columns {missing} which is smaller than the {multiple_removed_confidence} confidence with {previously_removed} columns removed')

        if acc >= norma_accuracy:
            print(f'Got accuracy of {acc} with missing columns {missing} which is bigger than the normal accuracy {norma_accuracy}')

        if acc <= multiple_removed_accuracy:
            print(f'Got accuracy of {acc} with missing columns {missing} which is smaller than the {multiple_removed_accuracy} accuracy with {previously_removed} columns removed')