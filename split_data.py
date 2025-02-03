import pandas as pd
import os
import re
import random


def read_all_save_unique(df):

    tmp = df.copy().drop('File', axis = 1)
    tmp = tmp.drop_duplicates()

    #jk duplicates can be on different days
    #fdf = tmp.merge(df, how = 'left', on = ['Subject', 'Predicate', 'Object'])
    return tmp  


def shuffle_save(df, type_val, output_dir):
    # Shuffle the data
    df = df.sample(frac=1).reset_index(drop=True)

    # Split the data
    train_size = int(0.8 * len(df))
    validation_size = int(0.1 * len(df))
    test_size = len(df) - train_size - validation_size

    train_df = df.iloc[:train_size]
    validation_df = df.iloc[train_size:train_size+validation_size]
    test_df = df.iloc[train_size+validation_size:]

    train_df = train_df.drop('File', axis = 1)
    validation_df = validation_df.drop('File', axis = 1)
    test_df = test_df.drop('File', axis = 1)

    # Save the data
    if not os.path.isfile(f'{output_dir}/train.tsv'):
        train_df.to_csv(f'{output_dir}/train.tsv', header=False, sep = '\t', index = False)
    else:
        train_df.to_csv(f'{output_dir}/train.tsv', mode='a', sep='\t', header=False, index=False)

    if not os.path.isfile(f'{output_dir}/validation.tsv'):
        validation_df.to_csv(f'{output_dir}/validation.tsv', header=False, sep = '\t', index = False)
    else:
        validation_df.to_csv(f'{output_dir}/validation.tsv', mode='a', sep='\t', header=False, index=False)

    if not os.path.exists(f'{output_dir}/test.tsv'):
        test_df.to_csv(f'{output_dir}/test.tsv', header=False, sep = '\t', index = False)
    else:
        test_df.to_csv(f'{output_dir}/test.tsv', mode='a', sep='\t', header=False, index=False)


def shuffle_save_unique(df, type_val, output_dir):

    #make dirs
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Shuffle the data
    df = df.sample(frac=1).reset_index(drop=True)

    # Split the data
    train_size = int(0.8 * len(df))
    validation_size = int(0.1 * len(df))
    test_size = len(df) - train_size - validation_size

    train_df = df.iloc[:train_size]
    validation_df = df.iloc[train_size:train_size+validation_size]
    test_df = df.iloc[train_size+validation_size:]

    # Save the data
    if not os.path.isfile(f'{output_dir}/train.tsv'):
        train_df.to_csv(f'{output_dir}/train.tsv', header=False, sep = '\t', index = False)
    else:
        train_df.to_csv(f'{output_dir}/train.tsv', mode='a', sep='\t', header=False, index=False)

    if not os.path.isfile(f'{output_dir}/validation.tsv'):
        validation_df.to_csv(f'{output_dir}/validation.tsv', header=False, sep = '\t', index = False)
    else:
        validation_df.to_csv(f'{output_dir}/validation.tsv', mode='a', sep='\t', header=False, index=False)

    if not os.path.exists(f'{output_dir}/test.tsv'):
        test_df.to_csv(f'{output_dir}/test.tsv', header=False, sep = '\t', index = False)
    else:
        test_df.to_csv(f'{output_dir}/test.tsv', mode='a', sep='\t', header=False, index=False)


def get_unique_entities(output_dir = ''):

    df1 = pd.read_csv(f"{output_dir}/train.tsv", sep = "\t", header =None)
    df2 = pd.read_csv(f"{output_dir}/validation.tsv", sep = "\t", header =None)
    df3 = pd.read_csv(f"{output_dir}/test.tsv", sep = "\t", header =None)

    df = pd.concat([df1, df2, df3])

    assert df.shape[0] == df1.shape[0] + df2.shape[0] + df3.shape[0]
    
    # Extract unique entities
    subject_entities = df[0].unique()
    predicate_entities = df[1].unique()

    print(subject_entities)

    # Save unique entities to tsv files
    pd.DataFrame(subject_entities, columns=[0]).to_csv(os.path.join(output_dir, 'entities.tsv'), sep='\t', index=False, header=False)
    pd.DataFrame(predicate_entities, columns=[0]).to_csv(os.path.join(output_dir, 'predicate.tsv'), sep='\t', index=False, header=False)


if __name__ == '__main__':
    # Load the TSV file
    tsv_dir = "tsv_dir"
    df = pd.read_csv(os.path.join(tsv_dir, "pharmacy_output_data.tsv"), sep='\t')
    read_all_save_unique(df).to_csv(os.path.join(tsv_dir, "pharmacy_unique.tsv"), sep='\t', index=False)

    # Shuffle and save the data
    #shuffle_save(df, 'pharmacy', 'transe-input')

    df = pd.read_csv(os.path.join(tsv_dir, "patient_output_data.tsv"), sep='\t')
    read_all_save_unique(df).to_csv(os.path.join(tsv_dir, "patient_unique.tsv"), sep='\t', index=False)
    #shuffle_save(df, 'patient', 'transe-input')

    df = pd.read_csv(os.path.join(tsv_dir, "imaging_output_data.tsv"), sep='\t')
    read_all_save_unique(df).to_csv(os.path.join(tsv_dir, "imaging_unique.tsv"), sep='\t', index=False)
    #shuffle_save(df, 'imaging', 'transe-input')

    # Load the TSV file
    #df = pd.read_csv(os.path.join(tsv_dir, "pharmacy_output_data.tsv"), sep='\t')

    #get_unique_entities('transe-input')


    # load files
    df = pd.read_csv(os.path.join(tsv_dir, "pharmacy_unique.tsv"), sep='\t')
    shuffle_save_unique(df, 'pharmacy', 'transe-input-unique')


    df = pd.read_csv(os.path.join(tsv_dir, "patient_unique.tsv"), sep='\t')
    shuffle_save_unique(df, 'patient', 'transe-input-unique')

    df = pd.read_csv(os.path.join(tsv_dir, "imaging_unique.tsv"), sep='\t')
    shuffle_save_unique(df, 'imaging', 'transe-input-unique')

