import pandas as pd

# Read the CSV files
group_members_df = pd.read_csv('group_members.csv')  # Replace with your actual file path
change_log_df = pd.read_csv('changes.csv')  # Replace with your actual file path

# Convert datetime strings to datetime objects
change_log_df['datetime'] = pd.to_datetime(change_log_df['datetime'])

# Prompt for a datetime input
# input_datetime_str = input("Enter a datetime (YYYY-MM-DD HH:MM:SS): ")
input_datetime_str = "2022-12-01 12:12:13"
input_datetime = pd.to_datetime(input_datetime_str)

# Filter change log entries before or equal to the specified datetime
filtered_change_log = change_log_df[change_log_df['datetime'] >= input_datetime]

# Apply changes to group members
for _, row in filtered_change_log.iterrows():
    if row['action'] == 'add':
        group_members_df = group_members_df._append({'username': row['username'], 'group': row['group']}, ignore_index=True)
    elif row['action'] == 'remove':
        index_to_remove = group_members_df.index[group_members_df['username'] == row['username']].tolist()[0]
        group_members_df = group_members_df.drop(index_to_remove)

with open('output.csv', 'w') as f:
    f.write(group_members_df.to_csv(index=False))

# Create a document showing the differences
output_filename = 'group_membership_changes.txt'
with open(output_filename, 'w') as output_file:
    output_file.write(f"Group membership changes at {input_datetime}:\n")
    output_file.write("=========================================\n")
    output_file.write(group_members_df.to_string(index=False))

print(f"Group membership changes saved to {output_filename}")
