import streamlit as st
import pandas as pd
from datetime import datetime
from prompts import merge_prompt, cleaning_prompt, rephrase_query_prompt, column_rename_prompt, update_query_prompt
from utils import get_agent, rephrase_query

state = st.session_state

if "submitted" not in state:
    state.submitted = False


def load_csv_files(uploaded_files):

    dataframes = []
    for file in uploaded_files:
        try:
            df = pd.read_csv(file)
            dataframes.append(df)
        except Exception as e:
            st.error(f"Error loading {file.name}: {e}")
    return dataframes

query_agent = get_agent(
                    dataframes=pd.DataFrame(),
                    prefix="""Assume all the dataframes are already loaded in the environment. If not found use 'updated_dataframe.csv' CSV file and load it.""",
                    suffix= """Don't print the 'df' as it would be more than your context window size.
                                If you don't find the answer in one go, try to modeify/adjust the query based on the data and column names and try again, You should retry 3 times in that case."""
                )

def pre_process(dataframes):
    
    merge_df_agent = get_agent(
                        dataframes=dataframes, 
                        prefix="",
                        suffix= "Don't print the 'df' as it would be more than your context window size."
                    )
    cleaning_agent = get_agent(
                            dataframes=pd.DataFrame(),
                            prefix="Assume all the dataframes are already loaded in the environment.",
                            suffix= "Don't print the 'df' as it would be more than your context window size."
                        )

    merge_df_agent.invoke(merge_prompt)
    cleaning_agent.invoke(column_rename_prompt)
    cleaning_agent.invoke(cleaning_prompt)
    
    df = pd.read_csv("updated_dataframe.csv")
    
    return df

def main():

    try:
        st.title("Data Cleaning and Query Engine")

        # Step 1: File Upload
        st.header("Upload CSV Files")
        uploaded_files = st.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)

        if uploaded_files:
            dataframes = load_csv_files(uploaded_files)
            st.success(f"Successfully loaded {len(dataframes)} file(s).")

            # Step 2: Display DataFrames
            st.header("Uploaded Files Preview")
            for df in dataframes:
                st.dataframe(df.head())  # Display the first few rows of each dataframe

            if not state.submitted:
                df = pre_process(dataframes=dataframes)
                
            df = df.sample(frac = 1)

            # Step 3: Query Box
            st.header("Query the Data")
            query = st.text_input("Enter your query regarding the uploaded files:",
                                on_change=lambda: state.update(submitted=True))
            
            if query:
                # Process query here. Placeholder message for now.
                st.write("Generating response...")
                updated_query = rephrase_query(update_query_prompt, query, current_time=datetime.now())
                print(f"{updated_query=}")
                rephrased_query = rephrase_query(rephrase_query_prompt, updated_query, df=df.head(n=5).to_json(orient='records', lines=True))
                print(f"{rephrased_query=}")
                output = query_agent.invoke(rephrased_query)
                output = output.get("output", "Try again!")
                st.write(output)

    except Exception as ex:
        raise ex

if __name__ == "__main__":
    main()
