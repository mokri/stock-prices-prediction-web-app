# IMPORT THE LIBRARIES....
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import warnings

warnings.filterwarnings("ignore")


def prepare_dataset(df):
    #  Selecting line by line from dataframe
    #  Odd rows as input
    #  Close price from even rows as output
    # df = df.reset_index(drop=True)
    # df = dframe.set_index('Open', inplace=True)

    # df.index = df['Open']

    df_1 = df.iloc[range(0, len(df), 2)]
    # df_1 = df_1.drop(df_1.index[-1])

    a = [i for i in range(0, len(df)) if i % 2 != 0]
    df_2 = df.iloc[a]

    if len(df_1) > len(df_2):
        df_1 = df_1.drop(df.tail(1).index)

    if len(df_1) < len(df_2):
        df_2 = df_2.drop(df.tail(1).index)

    # Insert the close price column in the dataframe 'df_1'

    # df_1.insert(6, 'out', df_2['Close'].to_list())

    # #### remove the date column
    #

    df_1.pop('Dividends')
    df_1.pop('Stock Splits')
    df_1.pop('Close')
    # y = df_1.pop('out')
   #  df_2.reset_index(drop=True, inplace=True)
   #  df_1 = df_1.reset_index()
    y = df_2['Close']  # ['Close'].to_list()
    X = df_1

    return X, y


# #### Split data on Train and Test

def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
    return X_train, X_test, y_train, y_test


def train(x_train, y_train):
    poly_feat = PolynomialFeatures(degree=1)
    X_poly = poly_feat.fit_transform(x_train)
    poly_model = LinearRegression(fit_intercept=False).fit(X_poly, y_train)
    return poly_model, poly_feat


# test = poly_feat.fit_transform(X_test)
# poly_model.score(test, y_test)


def predict(data, model, model_feat):
    # data must be a list
    # data = [X_test.iloc[s].to_list()]
    predict_ = model_feat.fit_transform(data)
    predict = model.predict(predict_)
    return predict[0]


def tomorrow_predictions(df):
    data = df.iloc[-1:]
    data = data.iloc[0].to_list()[:-2]
    del data[3]
    input_data, output_data = prepare_dataset(df)
    X_train, X_test, y_train, y_test = split_data(input_data, output_data)
    model, model_feat = train(X_train, y_train)
    return predict([data], model, model_feat)
    #
    # predicted_results = predict(data, model)
    # return predicted_results
