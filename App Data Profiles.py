# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 09:24:29 2019

@author: Thomas Tessier

Guided DataQuest Project : Analyzing App Data to determine profitable app profiles
"""
#%%
#Functions Cell

def explore_data(dataset, start, end, rows_and_columns=False):
    '''
    Print given rows of data to make it easier to read and examine
    '''
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

def english_string(text):
    '''
    take in a string and return a boolean True if using english characters and False if more than three non-english characters
    '''
    error=0
    for char in text:
        if ord(char) > 127:
            error+=1
            if error == 4:
                return False
    return True


def remove_duplicates(data,name,reviews):
    '''
    Take in a dataset and index of the name and reviews field, remove duplicates and return cleaned set keeping only version with most reviews
    '''
    dataset=data.copy()
    duplicate_apps={}
    unique_apps={}
    for index in range(len(dataset)):
        if dataset[index][name] in unique_apps:
            duplicate_apps[dataset[index][name]]=unique_apps[dataset[index][name]]
            duplicate_apps[dataset[index][name]].append(index)
        else:
            unique_apps[dataset[index][name]]=[index]
            
    remove_indices=[]
    for app in duplicate_apps:
        most_reviews=-1
        best_index=-1
        for index in duplicate_apps[app]:
            if float(dataset[index][reviews]) > most_reviews:
                most_reviews=float(dataset[index][reviews])
                if best_index != -1:
                    remove_indices.append(best_index)
                best_index=index
            else:
                remove_indices.append(index)
    remove_indices=sorted(remove_indices,reverse=True)
    for index in remove_indices:
        del(dataset[index])
    return dataset


def english_clean(data,name):
    dataset=data.copy()
    for index in range(len(dataset)-1,-1,-1):
        if not english_string(dataset[index][name]):
            del(dataset[index])
    return(dataset)


def free_clean(data,price):
    dataset=data.copy()
    for index in range(len(dataset)-1,-1,-1):
        if dataset[index][price] != '0':
            del(dataset[index])
    return dataset

def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
        
        
def freq_table(dataset,index):
    results={}
    for row in dataset:
        if row[index] in results:
            results[row[index]]+=1
        else:
            results[row[index]]=1
    for key in results:
        results[key]=results[key]/len(dataset)*100
    return results
#%%
#Program Cell

from csv import reader
with open('AppleStore.csv',encoding='utf8') as file:
    read_file=reader(file)
    Apple=list(read_file)
with open('googleplaystore.csv',encoding='utf8') as file:
    read_file=reader(file)
    Google=list(read_file)

#Data Cleaning
del(Google[10473])
#Removing Header Rows
del(Google[0])
del(Apple[0])



GoogleNoDups=remove_duplicates(Google,0,3)
AppleNoDups=remove_duplicates(Apple,2,6)



GoogleEng=english_clean(GoogleNoDups,0)
AppleEng=english_clean(AppleNoDups,2)



GoogleClean=free_clean(GoogleEng,7)
AppleClean=free_clean(AppleEng,5)


AppleGenre=sorted(list(freq_table(AppleEng,12).keys()))
for genre in AppleGenre:
    total=0
    len_genre=0
    for app in AppleClean:
        app_genre=app[12]
        if app_genre==genre:
            total+=float(app[6])
            len_genre+=1
    print(genre,'Total Ratings - ',total, '   Number of apps - ',len_genre)