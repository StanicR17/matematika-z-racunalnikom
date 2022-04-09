import pandas as pd
import numpy as np
import random
import statistics
from sklearn.linear_model import LinearRegression
import time
from Metrics import Metrics


data = pd.read_excel("C:\\Users\\1roks\\Documents\\FMF\Matematika z računalnikom\\Project\\Data\\Final data\\Final_data.xlsx")
# Izberi nakjlučni vzorec velikosti 300

# Clean sample

data_test = data[data.Train_test_identificator == "test"]
data_train = data[data.Train_test_identificator == "train"]


data_train = data_train.reset_index()
data_test = data_test.reset_index()


group_data = pd.read_excel("C:\\Users\\1roks\\Documents\\FMF\Matematika z računalnikom\\Project\\Data\\Final data\\Group_Data.xlsx")

decili_ccm_kw = pd.read_excel("C:\\Users\\1roks\\Documents\\FMF\Matematika z računalnikom\\Project\\Data\\Final data\\decili_ccm_kw.xlsx")
decili_ccm = list(decili_ccm_kw["decili_ccm"].values)
decili_kw = list(decili_ccm_kw["decili_kw"].values)

def is_nan(n):
    if str(n) == "nan":
        return True
    return False


# Definiraj funkcije za primerjavo

def primerjava_tipa(avto_main_tip, avto_main_znamka, avto_comp_tip, avto_comp_znamka, alfa_tip):
    # Če sta enaka vrni alfa
    if avto_main_tip == avto_comp_tip and avto_main_znamka == avto_comp_znamka:
        return alfa_tip
    
    # Če nista poglej, če imata oba count večji od 3
    
    main_data = group_data[(group_data.tip == avto_main_tip) & (group_data.znamka == avto_main_znamka)]
    
    comp_data = group_data[(group_data.tip == avto_comp_tip) & (group_data.znamka == avto_comp_znamka)]
    
    if len(main_data.index) > 0 and len(comp_data.index) > 0:
        main_mean = main_data["mean"].values[0]
        comp_mean = comp_data["mean"].values[0]
        
        rel_diff = abs((comp_mean - main_mean) / main_mean)
        
        return (1-rel_diff) * alfa_tip
    
    return 0

def primerjava_starosti(main_prva_reg, comp_prva_reg, alfa_starost):
    if is_nan(main_prva_reg) == False and is_nan(comp_prva_reg) == False:
        diff = min(abs(main_prva_reg-comp_prva_reg),30)
        return (30 - diff) * alfa_starost
    return 0

def primerjava_ccm(main_ccm_class, comp_ccm_class, alfa_ccm):
    if is_nan(main_ccm_class) == False and is_nan(comp_ccm_class)== False: 
        diff = 10- abs(main_ccm_class - comp_ccm_class)
        return diff *alfa_ccm
    return 0

def primerjava_kw(main_kw_class, comp_kw_class, alfa_kw):
    if is_nan(main_kw_class) == False and is_nan(comp_kw_class)== False: 
        diff = 10- abs(main_kw_class - comp_kw_class)
        return diff *alfa_kw
    return 0

def primerjava_prevozeni_km(main_km, comp_km, alfa_km):
    if is_nan(main_km) == False and is_nan(comp_km)== False:
        diff = abs(main_km-comp_km)
        diff = min(diff, 300000)
        return alfa_km * (300000 - diff)
    return 0

def primerjava_goriva(main_gorivo, comp_gorivo, alfa_gorivo):
    if is_nan(main_gorivo) == False and is_nan(comp_gorivo)== False:
        if main_gorivo == comp_gorivo:
            return alfa_gorivo
    return 0

def primerjava_menjalnik(main_menjalnik, comp_menjalnik, alfa_menjalnik):
    if is_nan(main_menjalnik) == False and is_nan(comp_menjalnik)== False:
        if main_menjalnik == comp_menjalnik:
            return alfa_menjalnik
    return 0

def primerjava_oblika(main_oblika, comp_oblika, alfa_oblika):
    if is_nan(main_oblika) == False and is_nan(comp_oblika)== False:
        if main_oblika == comp_oblika:
            return alfa_oblika
    return 0
    
    
def primerjava_barva(main_barva, comp_barva, alfa_barva):
    if is_nan(main_barva) == False and is_nan(comp_barva)== False:
        if main_barva == comp_barva:
            return alfa_barva
    return 0

# Izracunaj linearno regresijo


import pandas as pd
import numpy as np
import random
import statistics
from sklearn.linear_model import LinearRegression
import time
from sklearn import linear_model
import statsmodels.api as sm
import statistics as stats

min_cena = data_train["cena"].quantile(0.1)
max_cena = data_train["cena"].quantile(0.9)
data_train_for_univariate_linear_regression = data_train[(data_train.cena > min_cena) &  (data_train.cena < max_cena) ]

# Fit starost

data_train_for_multivariate_linear_regression_starost = data_train_for_univariate_linear_regression.dropna(subset=['starost'])

X_starost = data_train_for_multivariate_linear_regression_starost[['starost']] # here we have 2 variables for multiple regression. If you just want to use one variable for simple linear regression, then use X = df['Interest_Rate'] for example.Alternatively, you may add additional variables within the brackets
Y_starost = data_train_for_multivariate_linear_regression_starost['cena']

regr_starost  = linear_model.LinearRegression()
regr_starost.fit(X_starost, Y_starost)

# Fit prevozeni_km

data_train_for_multivariate_linear_regression_prevozeni_km = data_train_for_univariate_linear_regression.dropna(subset=['prevozeni_km'])

X_prevozeni_km = data_train_for_multivariate_linear_regression_prevozeni_km[['prevozeni_km']] # here we have 2 variables for multiple regression. If you just want to use one variable for simple linear regression, then use X = df['Interest_Rate'] for example.Alternatively, you may add additional variables within the brackets
Y_prevozeni_km = data_train_for_multivariate_linear_regression_prevozeni_km['cena']

regr_prevozeni_km  = linear_model.LinearRegression()
regr_prevozeni_km.fit(X_prevozeni_km, Y_prevozeni_km)

# Fit ccm_class

data_train_for_multivariate_linear_regression_ccm_class = data_train_for_univariate_linear_regression.dropna(subset=['ccm_class'])

X_ccm_class = data_train_for_multivariate_linear_regression_ccm_class[['ccm_class']] # here we have 2 variables for multiple regression. If you just want to use one variable for simple linear regression, then use X = df['Interest_Rate'] for example.Alternatively, you may add additional variables within the brackets
Y_ccm_class = data_train_for_multivariate_linear_regression_ccm_class['cena']

regr_ccm_class  = linear_model.LinearRegression()
regr_ccm_class.fit(X_ccm_class, Y_ccm_class)

def Model_no_adjustments(train_data, test_data, parameters, number_of_neighbours = 5,run_name = None, save_name =None, save_results = False, save_directory="C:\\Users\\1roks\\Documents\\FMF\\Matematika z računalnikom\\Project\\Data\\Modeling results\\"):
    
    # Initialize parameters
    alfa_tip = parameters[0]
    alfa_starost = parameters[1]
    alfa_ccm = parameters[2]
    alfa_kw = parameters[3]
    alfa_km = parameters[4] # Rationale 100,000 km je prbližno enako 3 leta starosti
    alfa_gorivo = parameters[5]
    alfa_menjalnik = parameters[6]
    alfa_oblika = parameters[7]
    alfa_barva = parameters[8]
    
    # Define empty list to save data
    out = []
    
    # Merge with group data
    
    train_data = pd.merge(train_data, group_data, on=["tip", "znamka"], how = "left")
    test_data = pd.merge(test_data, group_data, on=["tip", "znamka"], how = "left")
    
    
    train_data = train_data.reset_index()
    test_data = test_data.reset_index()
    # Loop through all cars to be evaluated
    for i in range(0,len(test_data.index)):
    
        mere_podobnosti = []
        tip = []
        starost = []
        ccm = []
        kw = []
        km = []
        gorivo = []
        menjalnik = []
        oblika = []
        barva = []
        
        # Filter out cars that have average price +- 20 %
        filter_out_value = 1.5
        avg_price_main = test_data["mean"].values[i]
        
        try:
            avg_price_main = float(avg_price_main)
            train_data_for_specific_car = train_data[(train_data.cena < avg_price_main * (1+filter_out_value)) & (train_data.cena > avg_price_main * (1-filter_out_value))]
        except ValueError:
            print("Mean price of car not available")
            train_data_for_specific_car = pd.DataFrame(train_data)
         
        # Če smo obdržali dovolj veliko število avtomobilov, potem nadaljujemo, če ne glejmo vse avtomobile
        if len(train_data_for_specific_car.index) < 50:
            train_data_for_specific_car = pd.DataFrame(train_data)
            
        
        train_data_for_specific_car = train_data_for_specific_car.reset_index(drop=True)
        
        for j in range(0,len(train_data_for_specific_car.index)):

            podobnost = 0

            # Primerjava Tipa

            avto_main_tip = test_data["tip"].values[i]
            avto_main_znamka = test_data["znamka"].values[i]
            avto_comp_tip = train_data_for_specific_car["tip"].values[j]
            avto_comp_znamka = train_data_for_specific_car["znamka"].values[j]

            p = primerjava_tipa(avto_main_tip, avto_main_znamka, avto_comp_tip, avto_comp_znamka, alfa_tip)
            tip.append(p)
            podobnost += p

            # Primerjava starosti

            main_prva_reg =  test_data["leto_prve_registracije"].values[i]
            comp_prva_reg =  train_data_for_specific_car["leto_prve_registracije"].values[j]

            p =  primerjava_starosti(main_prva_reg, comp_prva_reg, alfa_starost)
            starost.append(p)
            podobnost += p     

            # Primerjava ccm

            main_ccm = test_data["ccm_class"].values[i]
            comp_ccm = train_data_for_specific_car["ccm_class"].values[j]

            p = primerjava_ccm(main_ccm, comp_ccm, alfa_ccm)
            ccm.append(p)
            podobnost += p

            # Primerjava kw

            main_kw =  test_data["kw_class"].values[i]
            comp_kw = train_data_for_specific_car["kw_class"].values[j]

            p = primerjava_kw(main_kw, comp_kw, alfa_kw)
            kw.append(p)
            podobnost += p

            # Prevozeni km

            main_km =  test_data["prevozeni_km"].values[i]
            comp_km = train_data_for_specific_car["prevozeni_km"].values[j]

            p = primerjava_prevozeni_km(main_km, comp_km, alfa_km)
            km.append(p)
            podobnost += p

            # Primerjava gorivo

            main_gorivo =  test_data["gorivo"].values[i]
            comp_gorivo = train_data_for_specific_car["gorivo"].values[j]

            p = primerjava_goriva(main_gorivo, comp_gorivo, alfa_gorivo)
            gorivo.append(p)
            podobnost += p


            # Menjalnik

            main_menjalnik = test_data["menjalnik"].values[i]
            comp_menjalnik =train_data_for_specific_car["menjalnik"].values[j]

            p = primerjava_menjalnik(main_menjalnik, comp_menjalnik, alfa_menjalnik)
            menjalnik.append(p)
            podobnost += p

            # Oblika

            main_oblika= test_data["oblika"].values[i]
            comp_oblika = train_data_for_specific_car["oblika"].values[j]

            p = primerjava_oblika(main_oblika, comp_oblika, alfa_oblika)
            oblika.append(p)
            podobnost += p

            # Barva

            main_barva = test_data["barva"].values[i]
            comp_barva = train_data_for_specific_car["barva"].values[j]


            p =  primerjava_barva(main_barva, comp_barva, alfa_barva)
            barva.append(p)
            podobnost += p

            # Konec primerjav

            mere_podobnosti.append(podobnost)

        train_data_for_specific_car["mere_podobnosti"] = mere_podobnosti
        train_data_for_specific_car["atribut_tip"] = tip 
        train_data_for_specific_car["atribut_starost"] =starost
        train_data_for_specific_car["atribut_ccm"] = ccm 
        train_data_for_specific_car["atribut_kw"] =kw 
        train_data_for_specific_car["atribut_prev_km"] =km 
        train_data_for_specific_car["atribut_gorivo"] =gorivo 
        train_data_for_specific_car["atribut_menjalnik"] =menjalnik 
        train_data_for_specific_car["atribut_oblika"] = oblika 
        train_data_for_specific_car["atribut_barva"] =barva 


        comparable_cars = train_data_for_specific_car.sort_values(by= "mere_podobnosti", ascending =False)

        comparable_cars_final_candidates = comparable_cars.head(number_of_neighbours)
        
        IDS_comp = comparable_cars_final_candidates["ID"].values
        valuation = comparable_cars_final_candidates["cena"].mean()

    return valuation 


parametri = [466.08948962340173, 66.31282221516274, 8.032452666952638, 24.750775012632552, 0.0003428115825366971, 15.163346734039667, 10.564472529982988, 24.706757162345852, 0.5105554347604646]
	

