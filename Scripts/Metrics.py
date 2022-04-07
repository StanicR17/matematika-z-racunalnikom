# Calculate model metrics

import statistics
import pandas as pd

def rel_error(data, alfa, col_name):
    stevec = 0
    for i in range(0,len(data.index)):
        abs_error = abs(data["cena"].iloc[i]-data[col_name].iloc[i])
        rel_error = abs_error / data["cena"].iloc[i]
        if rel_error < alfa:
            stevec +=1
    return stevec / len(data.index)


# Funkcija za računanje napovedne uspšenosti modela


def Metrics(data, Sample_name,col_name, parametri):
    
    
    
    if len(data.index) == 0:
        Metrics = {"Sample"  : Sample_name,
               "Count" : len(data.index),
               "Error within 5 %": 0,
               "Error within 10 %": 0,
               "Error within 15 %": 0,
               "Error within 20 %": 0,
               "Error within 25 %": 0,
               "Error within 30 %": 0,
               "Error within 35 %": 0,
               "Error within 40 %": 0,
               "Error within 45 %": 0,
               "Error within 50 %": 0,
               "Median Absolute Error": 0,
               "Mean Absolute Error" : 0,
               "Max Absolute Error" : 0,
               "Median Relative_error": 0,
               "Absolute Median Relative Error": 0,
               "Mean Abosolute Relative Error" : 0,
               "Max Absolute Relative Error" : 0,
               "Parameters_used" : parametri
              }
        
        return pd.DataFrame([Metrics])

    
    
    relative_error = abs(data["cena"]-data[col_name])/data["cena"]

    Metrics = {"Sample"  : Sample_name,
               "Count" : len(data.index),
               "Error within 5 %": rel_error(data, 0.05,col_name),
               "Error within 10 %": rel_error(data, 0.10,col_name),
               "Error within 15 %": rel_error(data, 0.15,col_name),
               "Error within 20 %": rel_error(data, 0.20,col_name),
               "Error within 25 %": rel_error(data, 0.25,col_name),
               "Error within 30 %": rel_error(data, 0.30,col_name),
               "Error within 35 %": rel_error(data, 0.35,col_name),
               "Error within 40 %": rel_error(data, 0.40,col_name),
               "Error within 45 %": rel_error(data, 0.45,col_name),
               "Error within 50 %": rel_error(data, 0.50,col_name),
               "Median Absolute Error": statistics.median(list(abs(data["cena"] - data[col_name]))),
               "Mean Absolute Error" : statistics.mean(list(abs(data["cena"] - data[col_name]))),
               "Max Absolute Error" : max(abs(data["cena"] - data[col_name])),
               "Median Relative_error": statistics.median(list((data[col_name] -  data["cena"])/ data["cena"])),
               "Median Absolute Relative Error": statistics.median(list(relative_error)),
               "Mean Abosolute Relative Error" : statistics.mean(list(relative_error)),
               "Max Absolute Relative Error" : max(list(relative_error)),
               "Parameters_used" : parametri
              }
    return pd.DataFrame([Metrics])
