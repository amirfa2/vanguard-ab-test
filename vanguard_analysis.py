import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import chi2_contingency
from scipy import stats


def rename_demo_columns(df):

    new_column_names = {
        "clnt_tenure_yr": "tenure_year",
        "clnt_tenure_mnth": "tenure_month",
        "clnt_age": "age",
        "gendr": "gender",
        "num_accts": "number_of_accounts",
        "bal": "balance",
        "calls_6_mnth": "calls_6_month",
        "logons_6_mnth": "logons_6_month"
    }
    df_renamed = df.rename(columns=new_column_names)

    return df_renamed

def plot_numerical(df, cols):
    height = 2*len(cols)
    fig, axs = plt.subplots(len(cols), 1, figsize=(5, height))
    k = 0

    if len(cols) > 1:
        for col in cols:
            if df.dtypes.astype(str)[col] == 'float64' or df.dtypes.astype(str)[col] == 'int64':
                sns.histplot(data=df, x=col, ax=axs[k])
            elif df.dtypes.astype(str)[col] == 'object':
                sns.countplot(data=df, x=col, ax=axs[k])
            k += 1
    else:
        col = cols[0]
        if df.dtypes.astype(str)[col] == 'float64' or df.dtypes.astype(str)[col] == 'int64':
            sns.histplot(data=df, x=col, ax=axs)
        elif df.dtypes.astype(str)[col] == 'object':
            sns.countplot(data=df, x=col, ax=axs)

    fig.tight_layout()

def create_correlation_matrix(df, cols_numerical):

    correlation_matrix = df[cols_numerical].corr()

# Setting up the matplotlib figure with an appropriate size
    plt.figure(figsize=(6, 5))

# Drawing the heatmap for the numerical columns
    sns.heatmap(round(correlation_matrix, 2), annot=True,
                cmap="coolwarm", vmin=-1, vmax=1)

    plt.title("Correlation Heatmap for Selected Numerical Variables")
    plt.show()


def experiment_evalutaion(df):
    df["is_female"] = df["gender"].apply(lambda x: True if x == "F" else False)
    df_pivot = df.pivot_table(index='variation',
                              values=['age', 'tenure_year', 'number_of_accounts',
                                      'balance', 'calls_6_month', 'logons_6_month', 'is_female'],
                              aggfunc="mean")
    print('Bias Test vs Control: ')
    variables = []
    biases = []
    for col in df_pivot.columns:
        bias = df_pivot.loc["Test"][col]/df_pivot.loc["Control"][col]-1
        variables.append(col)
        biases.append(bias)
    return pd.DataFrame({"variable": variables, "bias": biases})


def calculate_avg_daily_visits_per_time_period(df):
    visits_total = (df["Control"] + df["Test"])

    visits_1 = visits_total.loc[(visits_total.index <= 13)].mean()
    visits_2 = visits_total.loc[(visits_total.index <= 41) & (
        visits_total.index > 13)].mean()
    visits_3 = visits_total.loc[(visits_total.index > 41)].mean()

    print(f"Average Daily Visits")
    print(f"--------------------")
    print(f"In the last two weeks of March: {int(round(visits_1, 0))}")
    print(f"In April: {int(round(visits_2, 0))}")
    print(f"In May and June: {int(round(visits_3, 0))}")

def calculate_time_spent(df):
    # Sort values and drop duplicates
    df_sorted = df.sort_values(by=['visit_id', 'process_step', 'date_time'], ascending=[True, True, False])
    df_main = df_sorted.drop_duplicates(subset=['visit_id', 'process_step'], keep='first').reset_index(drop=True)
    
    # Split the data into Control and Test groups
    df_control = df_main[df_main['variation'] == 'Control'].reset_index(drop=True)
    df_test = df_main[df_main['variation'] == 'Test'].reset_index(drop=True)
    
    def calculate_step_times(df):
        # Create a dictionary to hold dataframes for each step
        steps = ['start', 'step_1', 'step_2', 'step_3', 'confirm']
        step_dfs = {step: df[df['process_step'] == step][['visit_id', 'date_time']].rename(columns={'date_time': f'date_time_{step}'}) for step in steps}
        
        # Merge step dataframes on 'visit_id'
        df_merged = step_dfs['start']
        for step in steps[1:]:
            df_merged = pd.merge(df_merged, step_dfs[step], on='visit_id', how='inner')
        
        # Calculate time spent for each step
        time_spent = {
            'step 1': (df_merged['date_time_step_1'] - df_merged['date_time_start']).mean().total_seconds(),
            'step 2': (df_merged['date_time_step_2'] - df_merged['date_time_step_1']).mean().total_seconds(),
            'step 3': (df_merged['date_time_step_3'] - df_merged['date_time_step_2']).mean().total_seconds(),
            'confirm': (df_merged['date_time_confirm'] - df_merged['date_time_step_3']).mean().total_seconds()
        }
        
        return time_spent
    
    # Calculate time spent for Control and Test groups
    time_spent_control = calculate_step_times(df_control)
    time_spent_test = calculate_step_times(df_test)
    
    # Create a summary dataframe
    time_spent_summary = pd.DataFrame({
        'step': ['step 1', 'step 2', 'step 3', 'confirm'],
        'Control (s)': [time_spent_control['step 1'], time_spent_control['step 2'], time_spent_control['step 3'], time_spent_control['confirm']],
        'Test (s)': [time_spent_test['step 1'], time_spent_test['step 2'], time_spent_test['step 3'], time_spent_test['confirm']]
    })
    
    return time_spent_summary

def compare_calls_vs_logons(df):
    """
    This function filters the data, groups by variation, 
    and displays the total number of calls and logons for each group.
    """
    # Filter out rows with 'unknown' variation
    df_filtered = df[df['variation'] != 'unknown']

    # Group by variation and calculate the sum of calls and logons
    calls_vs_logons = df_filtered.groupby('variation').agg({
        'calls_6_month': 'sum',
        'logons_6_month': 'sum'
    }).reset_index()

    # Round the values
    calls_vs_logons['calls_6_month'] = calls_vs_logons['calls_6_month'].round(0).astype(int)
    calls_vs_logons['logons_6_month'] = calls_vs_logons['logons_6_month'].round(0).astype(int)

    # Display the results for verification
    print(calls_vs_logons)

    # plotting
    plt.figure(figsize=(10, 6))

    bar_width = 0.4
    index = range(len(calls_vs_logons))

    # Bars for calls
    plt.bar(index, calls_vs_logons['calls_6_month'], bar_width, label='Calls', color='#87CEEB')

    # Bars for logons
    plt.bar([i + bar_width for i in index], calls_vs_logons['logons_6_month'], bar_width, label='Logons', color='#9370DB')

    # Add the total number of calls on the calls bars 
    for i in index:
        # Display total number of calls
        plt.text(i, calls_vs_logons['calls_6_month'][i] + 2000, f"{calls_vs_logons['calls_6_month'][i]}", ha='center', color='black')

        # Add the total number of logons on the logons bars
        plt.text(i + bar_width, calls_vs_logons['logons_6_month'][i] + 2000, f"{calls_vs_logons['logons_6_month'][i]}", ha='center', color='black')

    # Titles and labels
    plt.title('Total Calls and Logins')
    plt.xlabel('Variation')
    plt.ylabel('Total Count')
    plt.xticks([i + bar_width / 2 for i in index], calls_vs_logons['variation'])
    plt.legend(title='Action')

    plt.tight_layout()
    plt.show()


def data_explore(df):

    # check number of rows and columns
    shape = df.shape
    print("Number of rows:", shape[0])
    print("Number of columns:", shape[1])

    # check duplicates
    check_duplicates = df.duplicated().sum()
    print("Number of duplicates:", check_duplicates)

    # Create a summary DataFrame
    summary_df = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes,
        'Non-Null Count': df.notnull().sum(),
        'Missing Values': df.isnull().sum(),
        'Unique Values': df.nunique()
    })

    # Reset index to make 'Column' a regular column
    summary_df.reset_index(drop=True, inplace=True)

    # Display the summary DataFrame
    summary_df

    # check numerical columns
    numerical_columns = df.select_dtypes("number").columns
    print("\nNumerical Columns:", numerical_columns)

    # check categorical columns
    categorical_columns = df.select_dtypes("object").columns
    print("\nCategorical Columns:", categorical_columns)

    return summary_df