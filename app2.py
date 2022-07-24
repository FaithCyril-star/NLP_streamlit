import streamlit as st
from textblob import TextBlob
import pandas as pd
import altair as alt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
def to_dataframe(sent):
    sentiment_dict = {'polarity':sent.polarity,'subjectivity':sent.subjectivity}
    df = pd.DataFrame(sentiment_dict.items(),columns=['metric','value'])
    return df

def analyse_token(docx):
    analysis = SentimentIntensityAnalyzer()
    pos_list = []
    neg_list = []
    neu_list = []
    for i in docx.split():
        res = analysis.polarity_scores(i)['compound']
        if res>=0.1:
            pos_list.append(i)
            pos_list.append(res)
        elif res<= -0.1:
            neg_list.append(i)
            neg_list.append(res)
        else:
            neu_list.append(i)
    result = {'positives':pos_list,'negatives':neg_list,'neutral':neu_list}
    return result


def main():
    st.title("Sentiment Analyser")
    st.subheader("Hey! Welcome to Faith's Sentiment Analyser")

    menu = ["Home","About"]
    choice = st.sidebar.selectbox("Menu",menu)
    if choice == "Home":
        # st.subheader("This app will classify your text as positive, negative or neutral.")
        with st.form(key="nlpform"):
            raw_text = st.text_area("Enter Text Here")
            submit_button = st.form_submit_button(label = 'Process')

            #layout
            col1,col2 = st.columns(2)
            if submit_button:
                with col1:
                    st.info("Results")
                    sentiment = TextBlob(raw_text).sentiment
                    st.write(sentiment)

                    ##emoji
                    if sentiment.polarity > 0:
                        st.markdown("Sentiment::Positive 😃")
                    elif sentiment.polarity < 0:
                        st.markdown("Sentiment::Negative 😠")
                    else:
                        st.markdown("Sentiment::Neutral 😐")

                    #Dataframe
                    df_result = to_dataframe(sentiment)
                    st.dataframe(df_result)

                    #Visualise
                    c = alt.Chart(df_result).mark_bar().encode(x='metric',y='value',
                    color = 'metric')
                    st.altair_chart(c,use_container_width=True)
                with col2:
                    st.info("Sentiment")
                    tokens = analyse_token(raw_text)
                    st.write(tokens)
    else:
        st.subheader("About")
        st.write("This is basically an NLP project to classify text, including product reviews or social media comments as positive, negative or neutral.")
        st.write("The stack of this application was built with Streamlit in Python.")
        st.write("The NLP libraries used were TextBlob for general sentiment extraction and VaderSentiment for token analysis.")
        st.write("It was made by Faith Sobe Cyril....🙃")
        st.write('Here are my socials, feel free to connect')
        st.write("email : cyrifaith17@gmail.com")
        st.write("linkedin : https://www.linkedin.com/in/faith-cyril/")
        st.write("github : https://github.com/FaithCyril-star")
if __name__ == "__main__":
    main()