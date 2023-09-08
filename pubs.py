import streamlit as st
from pymed import PubMed
import pandas as pd
import base64 

def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Bytes to string conversion
    return f'<a href="data:file/csv;base64,{b64}" download="search_results.csv">Download CSV</a>'

# Function to run the PubMed query
def run_query(journals_selected, term_query, start_date, end_date):
    # Set up PubMed API client
    pubmed = PubMed(tool="MyTool")

    # Construct the journal query
    journal_query = " OR ".join([f'"{journal}"[jour]' for journal in journals_selected])
    
    # Construct the complete query string
    query = f'("{start_date}"[Date - Create]:"{end_date}"[Date - Create]) AND ({term_query}) AND ({journal_query})'

    # Execute the query
    results = pubmed.query(query, max_results=1000)
    
    articles_dict = {}
    for article in results:
        article_id = article.pubmed_id
        title = article.title
        keywords = '", "'.join([kw for kw in article.keywords if kw is not None]) if article.keywords else None
        publication_date = article.publication_date
        abstract = article.abstract

        article_dict = {
            "Title": title,
            "Journal": article.journal,
            "Publication Date": publication_date,
            "Abstract": abstract,
        }

        articles_dict[article_id] = article_dict
    
    return pd.DataFrame(list(articles_dict.values()), columns=["Title", "Journal", "Publication Date", "Abstract"])

# Define the main function for the Streamlit app
def main():
    st.title('PubMed Journal Search')

    # Predefined list of journals
    journal_options = [
        "Radiology",
        "Magnetic Resonance in Medicine",
        "Gastrointestinal Endoscopy",
        "American Journal of Roentgenology",
        "Human Brain Mapping",
        "American Journal of Neuroradiology",
        "Radiographics",
        "Journal of Magnetic Resonance Imaging",
        "Journal of American Society of Echocardiography",
        "JACC Cardiovascular Imaging"
    ]

    # Streamlit widgets to get user inputs
    st.write('## Select Journals:')
    journals_selected = st.multiselect('', journal_options, default=journal_options)
    
    st.write('## Input Search Terms:')
    st.write('Please input your search terms. For multiple terms, you can use logical operators like AND/OR. Use parentheses for complex logic.')
    term_query = st.text_area('', '(fibrosis OR steatosis) AND liver OR NAFLD OR NASH')
    
    st.write('## Select Date Range:')
    start_date = st.date_input("Start Date", pd.to_datetime('2020-01-01'))
    end_date = st.date_input("End Date", pd.to_datetime('2100-01-01'))
    
    # Button to execute the search
    if st.button('Search'):
        with st.spinner('Searching PubMed...'):
            df = run_query(journals_selected, term_query, start_date, end_date)
            st.dataframe(df,
                         hide_index=True)
            
            # Provide download link for the data
            st.markdown(get_table_download_link(df), unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == '__main__':
    main()
