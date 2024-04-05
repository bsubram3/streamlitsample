import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go

st.title("Data App Assignment")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)


# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

category_list = df['Category'].unique()
category_option = st.selectbox('Select Category', category_list)

#st.write('You selected:', category_option)

selected_category_df = df[df['Category']==category_option]

sub_category_list = selected_category_df['Sub_Category'].unique()
sub_category_option = st.multiselect('Select Sub Category', sub_category_list)
#st.write('Your sub category selected:', sub_category_option)
#st.text('selected_category_df')
#st.dataframe(selected_category_df)
if sub_category_option:
    selected_sub_category_df = selected_category_df[selected_category_df['Sub_Category'].isin(sub_category_option)]
    #st.text('selected_sub_category_df')
    #st.dataframe(selected_sub_category_df)
    #st.text('selected_sub_category_df1')
    sub_category_sales_by_month = selected_sub_category_df.filter(items=['Sales','Sub_Category'])
    #st.dataframe(sub_category_sales_by_month)
    #st.text('selected_sub_category_df2')
    #sub_category_sales_by_month = selected_sub_category_df.filter(items=['Sales','Sub_Category']).groupby( pd.Grouper(['Order_Date','Sub_Category'], freq='M'))['Sales'].sum().reset_index()
    sub_category_sales_by_month = selected_sub_category_df.groupby('Sub_Category').resample('ME').sum()
    #st.dataframe(sub_category_sales_by_month)
    sub_category_sales_by_month = sub_category_sales_by_month[['Sales','Profit','Discount']]
    #st.dataframe(sub_category_sales_by_month)
    #print(type(sub_category_sales_by_month))
    sub_category_sales_by_month.reset_index(inplace=True)
    #st.text('sub_category_sales_by_month')
    #st.dataframe(sub_category_sales_by_month)

    # Create traces for each category
    traces = []
    for sub_category in sub_category_sales_by_month['Sub_Category'].unique():
        sub_category_df = sub_category_sales_by_month[sub_category_sales_by_month['Sub_Category'] == sub_category]
        trace = go.Scatter(x=sub_category_df['Order_Date'], y=sub_category_df['Sales'], mode='lines', name=sub_category)
        traces.append(trace)

    # Create the figure
    fig = go.Figure(data=traces)

    # Add title and labels
    fig.update_layout(title='Monthly Sales by selected Subcategory',
                      xaxis_title='Month',
                      yaxis_title='Sales')


    # Display Plotly chart in Streamlit
    st.plotly_chart(fig)

    total_sales = sub_category_sales_by_month['Sales'].sum()
    total_profit = sub_category_sales_by_month['Profit'].sum()
    avg_profit = sub_category_sales_by_month['Profit'].mean()
    overall_avg_profit = df['Profit'].mean()
    profit_diff = total_profit / overall_avg_profit
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Overall Profit Margin (%)", f"{(total_profit/total_sales):.2%}", f"{profit_diff:,.2%}" )

#st.write("## Your additions")
#st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
#st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
#st.write("### (3) show a line chart of sales for the selected items in (2)")
#st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
#st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
