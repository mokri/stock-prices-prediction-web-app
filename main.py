import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from tomorrow_pred import tomorrow_predictions
from long_period_pred import next_x_days_pred
from stock_data import *


@st.cache
def charts(df, year):
    df = df[year:]
    date = pd.DataFrame(df.index)
    date['Date'] = date['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))

    df.insert(len(df.columns), 'Date', date['Date'].to_list())
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])

    fig.update_layout(width=900, height=600)
    return fig


@st.cache
def tomorrow_pred(df):
    date = pd.DataFrame(df.index)
    date['Date'] = date['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df.insert(len(df.columns), 'Date', date['Date'].to_list())

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])

    fig.update_layout(width=900, height=900)
    return fig


@st.cache
def get_years(df):
    date = pd.DataFrame(df.index)
    date['Date'] = date['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))

    return date['Date']


def main():
    st.title('Stock Prices Prediction Charts')

    st.info('Predicting the price of a given Stock for Tomorrow or the next \'x\' number of days')
    st.text('Check About section for more Information')

    menu = ['Home', 'About']
    menu_choice = st.sidebar.selectbox('Navigation', menu)

    activities = stock_symbols()
    stock_choice = ''
    data = 0
    if menu_choice == 'Home':
        stock_choice = st.selectbox('Select Stock', activities['symbol'] + ' - (' + activities['name'] + ')')

        st.subheader('Data:')
        if st.sidebar.checkbox('Show Dataframe'):
            with st.spinner('Wait for it...'):
                try:
                    data = get_data(stock_choice)
                except Exception:
                    print(Exception)
            st.success('Done!')
            st.dataframe(data)

        if st.sidebar.checkbox('Show Previous data Charts'):
            with st.spinner('Wait for it...'):
                chart = charts(get_data(stock_choice), 1000)

            st.success('Done!')
            years = st.selectbox('filter by year', get_years(get_data(stock_choice)))
            if years:
                with st.spinner('Wait for it...'):
                    chart = charts(get_data(stock_choice), years)
                st.write(chart)
            else:
                st.write(chart)

        if st.sidebar.checkbox('Show Tomorrow\'s prediction'):
            with st.spinner('Wait for it...'):
                pred = tomorrow_predictions(get_data(stock_choice))
            st.success('The price is expected to be: ' + '**' + str(pred) + '**' + ':dollar:')
            st.warning('**Note**: The price could be *greater/lesser* than the actual price by **$1** :dollar:')

        prediction_range = ['select', 'week', 'month', '6 months', 'year']
        range_choice = st.sidebar.selectbox('Show Predictions for The next:', prediction_range)
        if range_choice == 'week':
            st.spinner(text="In progress...")
            with st.spinner('Wait for it...'):
                next_week_pred, next_week_pred_chart = next_x_days_pred(get_data(stock_choice), 10)
            st.success('Done!, next week predictions')
            st.write(next_week_pred)
            st.write(next_week_pred_chart)
        elif range_choice == 'month':
            st.spinner(text="In progress...")
            with st.spinner('Wait for it...'):
                next_month_pred, next_month_pred_chart = next_x_days_pred(get_data(stock_choice), 33)

            st.success('Done!, next month predictions')
            st.write(next_month_pred)
            st.write(next_month_pred_chart)

        elif range_choice == '6 months':
            st.spinner(text="In progress...")
            with st.spinner('Wait for it...'):
                next_6month_pred, next_6month_pred_chart = next_x_days_pred(get_data(stock_choice), 183)

            st.success('Done!, next 6 months predictions')
            st.write(next_6month_pred)
            st.write(next_6month_pred_chart)

        elif range_choice == 'year':
            st.spinner(text="In progress...")
            with st.spinner('Wait for it...'):
                next_year_pred, next_year_pred_chart = next_x_days_pred(get_data(stock_choice), 368)

            st.success('Done!, next year predictions')
            st.write(next_year_pred)
            st.write(next_year_pred_chart)

    elif menu_choice == 'About':

        components.html(
            """
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

                  <div class="card border-secondary"> <div class="card-header" style="font-weight:bold;">About</div> 
                  <div> <span class="badge badge-warning">Python</span> <span class="badge 
                  badge-warning">Scikit-learn</span> <span class="badge badge-warning">plotly</span> <span class="badge 
                  badge-warning">streamlit</span> <span class="badge badge-warning">pandas</span> </div> <div 
                  class="card-body text-secondary"> <h5 class="card-title">Stock Prices Predictions Using Machine 
                  Learning. </h5> <p class="card-text" style="color:black">Chart of  given Stock history, 
                  and Predictions for it for <strong>Tomorrow</strong>, <strong> a Week</strong>, <strong>a 
                  Month</strong>, <strong>6 Months</strong> and for <strong> a year.</strong><br> 
                     
                     <div class="alert alert-danger" role="alert"> The Results of this application was predicted 
                     using Machine Learnig Models. So the results might be false! 
                        
                    </div> 
                    Credit: <a href="https://pypi.org/project/yfinance/" target="_blank">yfinance.</a>
                    <a href="https://pypi.org/project/prophet/" target="_blank">Prophet</a> 
                    </p> </div> </div> 


            """,
            height=350,
        )

        components.html(
            """
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

            <div class="card text-white bg-dark"> <div class="card-header">Find Me</div> <div class="card-body">
            <a href="https://abdelhakmokri.pythonanywhere.com/" class="badge badge-light">Website</a><br> 
            <a href="https://github.com/mokri" class="badge badge-light">Github</a> <br> 
            <a href="https://www.instagram.com/abdelhakmokri/" class="badge badge-light">Instagram</a> <br> 
            <a href="https://www.facebook.com/ABDELHAKMOKRI/" class="badge badge-light">Facebook</a> <br> 
            <a href="https://twitter.com/abdelhakmokri" class="badge badge-light">Twitter</a> <br> 
            <a href="https://www.linkedin.com/in/abdelheq-mokri-b55425160/" class="badge badge-light">Linkedin</a>
            <hr> 
                <p>Copyright &copy; <script>document.write(new Date().getFullYear())</script> Abdelheq Mokri</p>
            """,
            height=300,
        )


if __name__ == '__main__':
    main()
