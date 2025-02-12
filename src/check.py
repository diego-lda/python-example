import pandas as pd
import os
import io


def check_missing_values(df):
    missing_values = df.isnull().sum()
    return missing_values[missing_values > 0]

def check_duplicates(df):
    duplicate_rows = df[df.duplicated()]
    return duplicate_rows

def check_duplicates_subset(df):
    subset_columns = ['item_id', 'sale_price']
    duplicate_rows = df[df.duplicated(subset=subset_columns)]
    return duplicate_rows

def check_summary_statistics(df):
    summary_stats = df.describe(include='all')
    unique_counts = df.nunique()
    summary_stats.loc['unique'] = unique_counts
    return summary_stats

def generate_report(df):
    report = {}
    report['missing_values'] = check_missing_values(df)
    report['duplicates'] = check_duplicates(df)
    report['summary_statistics'] = check_summary_statistics(df)
    return report

def display_dataset_info(df):
    info_buffer = io.StringIO()
    df.info(buf=info_buffer)
    info_str = info_buffer.getvalue()
    
    first_rows = df.head().to_string()
    
    return info_str, first_rows

def save_report(report, file_path):
    with open(file_path, 'w') as f:
        f.write("Quality Assurance Report\n")
        f.write("========================\n\n")
        
        f.write("Dataset Information:\n")
        info_str, first_rows = display_dataset_info(df)
        f.write(info_str)
        f.write("\n\n")
        
        f.write("First few rows of the dataset:\n")
        f.write(first_rows)
        f.write("\n\n")
        
        f.write("Missing Values:\n")
        f.write(report['missing_values'].to_string())
        f.write("\n\n")
        
        f.write("Duplicate Rows:\n")
        if not report['duplicates'].empty:
            f.write(report['duplicates'].to_string())
        else:
            f.write("No duplicate rows found.")
        f.write("\n\n")
        
        f.write("Summary Statistics:\n")
        f.write(report['summary_statistics'].to_string())
        f.write("\n")

if __name__ == "__main__":
    file_path = '/Users/diegolara/guidance/live_example/python-example/data/master_sales.csv'
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        report = generate_report(df)
        duplicates_subset = check_duplicates_subset(df)
        save_report(report, '/Users/diegolara/guidance/live_example/python-example/data/quality_assurance_report.txt')
    else:
        print(f"File {file_path} does not exist.")