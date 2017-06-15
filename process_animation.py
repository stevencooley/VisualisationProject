import os
import glob
import pandas as pd

data_path = os.path.join(os.getcwd(), 'lsoa contact data')

glob_folder = os.path.join(data_path, '*.csv')
file_list = glob.glob(glob_folder)  # get a list of all files in the folder

bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
group_names = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

final_df = pd.DataFrame()

for file in file_list:

    results_data = pd.read_csv(file)
    filename = os.path.basename(file)[0:-4]
    year = filename[len(filename)-4:]
    results_data.columns = ['lsoa', 'value']

    results_data['cats'] = pd.cut(results_data['value'], bins, labels=group_names)
    int_series = results_data.groupby('cats').size()
    int_series.name = year

    final_df = pd.concat([final_df, int_series], axis=1)


final_df.index = group_names
print(final_df)
final_df = pd.DataFrame(final_df).T
final_df['sum'] = final_df.sum(axis=1)
print(final_df)
df_new = final_df.loc[:].div(final_df["sum"], axis=0)
df_new.drop(['sum'], axis=1, inplace=True)
df_new = df_new*100
df_new.sort_index(inplace=True)




pd.DataFrame.to_csv(df_new, "new.csv")

print(df_new)