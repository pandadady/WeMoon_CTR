# -*- coding:utf-8 -*-

"""
Based on TensorFlow2.0
Author:
    Qingzhongwen, VX: ziqingxiansheng
"""

import os
import pandas as pd
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import tensorflow as tf
from deep_models.keras_models.models.keras_wide_and_deep import Keras_WD
from deep_models.keras_models.layers.features_typy_dict import Categorical_Feature, Numeric_Feat


if __name__ == "__main__":
    data = pd.read_csv('./data/titanic/train.csv')

    categorical_colunms = ['sex', 'n_siblings_spouses', 'parch', 'class', 'deck', 'embark_town', 'alone']
    numeric_colunms= ['age', 'fare']

    data[categorical_colunms] = data[categorical_colunms].fillna('-1', )
    data[numeric_colunms] = data[numeric_colunms].fillna(0, )
    target = ['survived']

    for feat in categorical_colunms:
        lbe = LabelEncoder()
        data[feat] = lbe.fit_transform(data[feat])

    mms = MinMaxScaler(feature_range=(0, 1))
    data[numeric_colunms] = mms.fit_transform(data[numeric_colunms])

    categorical_features = [Categorical_Feature(feat, vocabulary_size=data[feat].nunique(), embedding_dim=8)
                            for feat in categorical_colunms]
    numeric_features = [Numeric_Feat(feat, 1, ) for feat in numeric_colunms]

    all_feature_columns_dic_list = numeric_features + categorical_features
    feature_names = categorical_colunms + numeric_colunms

    # split data
    train, test = train_test_split(data, test_size=0.2)
    train_model_input = {name:train[name] for name in feature_names}
    test_model_input = {name:test[name] for name in feature_names}

    # Call the pre_defined models
    model = Keras_WD(all_feature_columns_dic_list, task='binary')
    print(model.summary())
    model.compile("adam", "binary_crossentropy", metrics=['binary_crossentropy','accuracy'], )
    history = model.fit(train_model_input, train[target].values,
                        batch_size=256, epochs=200, verbose=2, validation_split=0.2, )

    output_dir = "./saved/keras_wd/1"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    # save model
    tf.saved_model.save(model, output_dir)
    # del model
    pred_ans = model.predict(test_model_input, batch_size=256)
    print("test LogLoss", round(log_loss(test[target].values, pred_ans), 4))
    print("test AUC", round(roc_auc_score(test[target].values, pred_ans), 4))






