import streamlit as st
import seaborn as sn
import preprocessor, helper
import matplotlib.pyplot as plt

st.sidebar.title("whatsapp chat Analyzer")

uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "overall")
    selected_user = st.sidebar.selectbox("show analysis wrt", user_list)
    st.title("TOP STATISTICS")
    if st.sidebar.button("Show analysis"):
        num_messages, word, num_media_messages,links = helper.fetch_stats(selected_user, df)
        col1, col2, col3 ,col4= st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(word)
        with col3:
            st.header("Total Media ")
            st.title(num_media_messages)
        with col4:
            st.header("Total links")
            st.title(links)
    #monthlytimeline
    st.title("Monthly Time")
    timeline=helper.monthly_timeline(selected_user,df)
    fig,ax=plt.subplots()
    plt.plot(timeline['time'],timeline['message'],color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    #daily timeline
    st.title("Daily Time")
    daily_timeline=helper.daily_timeline(selected_user,df)
    fig,ax=plt.subplots()
    plt.plot(daily_timeline['only_date'],daily_timeline['message'],color='Black')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    #ACTIVITY MAP
    st.title("Activity Map")
    col1,col2=st.columns(2)
    with col1:
        st.header("Most busy day")
        busy_day=helper.week_activity_map(selected_user,df)
        fig,ax=plt.subplots()
        ax.bar(busy_day.index,busy_day.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.header("Most busy Month")
        busy_month=helper.month_activity_map(selected_user,df)
        fig,ax=plt.subplots()
        ax.bar(busy_month.index,busy_month.values,color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


    # finding the busiest users in the group
    if selected_user=='overall':
        st.title("most busy users")
        x,new_df=helper.most_busy_user(df)
        fig,ax=plt.subplots()
        col1,col2=st.columns(2)
        with col1:
            ax.bar(x.index,x.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)
    
    # heat map
    st.title("Weekly Activity Heat Map ")
    user_heatmap=helper.activity_heatmap(selected_user,df)
    fig,ax=plt.subplots()
    ax=sn.heatmap(user_heatmap)
    st.pyplot(fig)


    st.title("Wordcloud")
    df_wc=helper.create_wordcloud(selected_user,df)
    fig,ax =plt.subplots()
    plt.imshow(df_wc)
    st.pyplot(fig)
    # most common words
    st.title("Common Words")
    most_df=helper.most_commonwords(selected_user,df)
    fig,ax=plt.subplots()
    ax.barh(most_df[0],most_df[1])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    st.dataframe(most_df)

    emoji_df=helper.emoji_helper(selected_user,df)
    st.title("Emoji Analysis")
    col1,col2=st.columns(2)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig,ax=plt.subplots()
        ax.pie(emoji_df[1].head(6),labels=emoji_df[0].head(6),autopct="%0.2f")
        st.pyplot(fig)
