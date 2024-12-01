merge_prompt = """You are an expert data analyst responsible for cleaning a Pandas DataFrame in Python. Follow these tasks precisely to enhance data quality:
    
    1. **Merge multiple dataframes**:
       - Examine each column in all the dataframes and merge the data frames on the column that shows relation between the two.
       - The merged dataframe must contain all the rows that exists in original data, not only first N rows.
     **Expected Output Format**:
    - Save the merged dataframe as merged_dataframe.csv file.
    """

cleaning_prompt = """
    You are an expert data analyst responsible for cleaning a Pandas DataFrame in Python. Follow these tasks precisely to enhance data quality:

    You must load the data from the 'renamed_df.csv' file to process it.
    Don't use any other dataframe that exists in your environment for this task.

    1. **Identify and Drop Insignificant Columns**
        - Examine each column in the DataFrame and identify columns that are not useful for analysis, such as:
            - You must be cautious about dropping a column and only drop the columns with no sognificance like IDs(Identifiers or serial number).
            - Columns with the same constant value or NaN values across all rows.
            - Columns with redundant or duplicate information.

    2. **Handle Missing Values**
        - For each column with missing values, suggest the most suitable method to handle them based on the data type and context:
            - Use "drop rows with null values" if the column is critical and cannot have missing values.
            - Use "fill with mean" or "fill with median" for numeric columns.
            - Use "fill with mode" for categorical columns.

    3. **Correct Data Inconsistencies**
        - For each column with data inconsistencies, identify and recommend appropriate corrections:
            - Standardize date formats (e.g., to "YYYY-MM-DD").
            - Standardize text data (e.g., convert to lowercase or uppercase for consistency).
            - Correct any obvious formatting issues (e.g., mixed data types).

    **Expected Output Format**:
    - Save the updated dataframe as updated_dataframe.csv file.
    """

column_rename_prompt = """You are an expert data analyst responsible for creating descriptive and business-friendly names for columns in 
    a pandas DataFrame in Python. Below is information about the data:
    
    You must load the data from the 'merged_dataframe.csv' file to process it.
    Don't use any other dataframe that exists in your environment for this task.

    - The data includes two primary files which is included in one pandas dataframe:
      1. **Airline ID to Name Mapping**: This file maps airline IDs to their respective airline names.
         Example columns: "airlie_id" (airline identifier), "airline_name" (full airline name).
      2. **Flight Bookings Data**: Contains detailed information about flight bookings, such as:
         - **Flight Details**: Flight number, departure and arrival dates/times.
         - **Passenger Information**: Booking code, passenger name, seat number, and class (e.g., Economy, Business).
         - **Amenities and Preferences**: Meal options, inflight entertainment availability, window or aisle seat preference, Wi-Fi availability.
         - **Crew and Other Details**: Crew information, pilot names, and reward program membership.
    
    Given this context and the first few rows of the data, generate clear, concise, and business-relevant names for each 
    column in `df_columns` that improve readability and make the data understandable for non-technical users. 

    Guidelines:
    - Avoid abbreviations unless well-known in business contexts (e.g., "ID" instead of "Identifier").
    - Use terms that reflect each column's specific business context, such as "Flight Number" or "Departure Date".
    - For date or time columns, specify if they relate to departure or arrival (e.g., "Departure Date", "Arrival Time").
    - Make numeric metrics self-explanatory (e.g., "Number of Stops", "Seat Preference").
    
    
     **Expected Output Format**:
    - Save the updated dataframe as renamed_df.csv file.
    """

update_query_prompt = """Your task is to identify all the date and time references within a given sentence.
If the user input sentence contains relative time frame you must calculate the relative time with respect to {current_time}
(The date time could be in any of these formats... 30th january 2023, last month, last week, 30-01-2024, yersterday, 
current time, etc.).

If the input query does not contain any time reference then give the input sentence as your output only and do not add anything else.

Refer to below examples:
input : List all the flights for 'alaska airlines' airline for last week.
output : List all the flights for 'alaska airlines' airline starting from 2024-04-23T23:54:13 to 2024-04-30T23:54:13.

Note: Here for example, we have assumed that the current time is 2024-04-30T23:54:13.
"""