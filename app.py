import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

st.sidebar.title("Github Repo Analysis")

uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    def clean_ts(df):
        return df[(df['author_timestamp'] > 1104600000) & (df['author_timestamp'] < 1487807212)]
    df = clean_ts(data)
    df['author_dt'] = pd.to_datetime(df['author_timestamp'],unit='s').dt.day
    time_df = df.groupby(['author_timestamp', 'author_dt'])[['n_additions', 'n_deletions']].agg(np.sum).reset_index().sort_values('author_timestamp', ascending=True)
    time_df['diff'] = time_df['n_additions'] - time_df['n_deletions']
    
    if st.sidebar.button("Show Analysis"):
        
        #1
        # lines of code added
        st.title("Lines of code added")
        t = pd.Series(time_df['diff'].values, index=time_df['author_dt'])
        st.line_chart(t, use_container_width=True)

        #2
        st.title("Number of Commits Over Time")
        # Number of commits on original time series
        # Group the data by author_dt and count the unique commit_hash values
        commits_over_time = df.groupby('author_dt')['commit_hash'].nunique().reset_index().sort_values('author_dt', ascending=True)
        # Create a pandas series from the commit_hash and author_dt columns
        commits_series = pd.Series(commits_over_time['commit_hash'].values, index=commits_over_time['author_dt'])
        # Plot the series
        fig2, ax = plt.subplots(figsize=(12,8))
        ax.plot(commits_series.index, commits_series.values)
        ax.set_title('Number of Commits Over Time')
        ax.set_xlabel('Author Date')
        ax.set_ylabel('Number of Commits')
        # Display the plot in Streamlit
        st.pyplot(fig2)

        #3
        st.title("Number of files changed per commit")
        # Number files changed per commit
        # Assuming that df is a pandas DataFrame with columns: author_dt, commit_hash, filename
        files_changed_per_commit = df.groupby(['author_dt', 'commit_hash'])['filename'].agg('count').reset_index().sort_values('author_dt', ascending=True)
        files_changed_per_commit = pd.Series(files_changed_per_commit['filename'].values, index=files_changed_per_commit['author_dt'])
        # Create a Streamlit figure object
        fig3, ax = plt.subplots(figsize=(12,8))
        # Plot the data
        files_changed_per_commit.plot(title='number files changed per commit', ax=ax)
        # Display the plot in Streamlit
        st.pyplot(fig3)
        
        #4
        st.title("Distribution of Number of Files Changed per Commit")
        # Assuming that the data has already been loaded into a pandas dataframe 'df'
        # Trim the distribution
        n_files_changed_per_commit = df.groupby('commit_hash')['filename'].agg('count')
        n_files_changed_per_commit = n_files_changed_per_commit[n_files_changed_per_commit < 20]
        # Plot the distribution using Seaborn
        fig4, ax = plt.subplots()
        sns.distplot(n_files_changed_per_commit, kde=False, ax=ax)
        ax.set_title('Distribution of Number of Files Changed per Commit')
        ax.set_xlabel('Number of Changed Files')
        # Display the plot using Streamlit
        st.pyplot(fig4)

        #5 additions_per_commit
        st.title('Additions per commit')
        # Calculate the sum of additions per commit
        additions_per_commit = df.groupby('commit_hash')['n_additions'].agg(np.sum)
        # Filter out commits with more than 100 additions
        additions_per_commit = additions_per_commit[additions_per_commit < 100]
        # Create a plot using Seaborn's distplot function
        fig5, ax = plt.subplots(figsize=(12, 8))
        sns.distplot(additions_per_commit, ax=ax)
        # Display the plot in Streamlit
        st.pyplot(fig5)
        
        #6 Commit Activity
        st.title('Commit Activity')
        df['subject_char_len'] = df['subject'].str.len()
        # calculate commit activity
        df['commit_activity'] = df['n_additions'] + df['n_deletions']
        # create Streamlit app
        # create heatmap
        cmap = plt.get_cmap('viridis')
        fig6, ax = plt.subplots()
        sns.heatmap(df[['commit_utc_offset_hours', 'commit_activity', 'subject_char_len']].corr(), cmap=cmap, ax=ax)
        # display the heatmap in Streamlit
        st.pyplot(fig6)





