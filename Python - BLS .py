#!/usr/bin/env python
# coding: utf-8

# In[108]:


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, request, redirect, url_for, flash, jsonify
import requests
import json
import pandas as pd
import argparse

app = Flask(__name__)
api = Api(app)

registrationkey = "0310114879de4413ad6b6f8de6e7764c"

class get_ui_data(Resource):
    def __init__ (self):
         self.parser = reqparse.RequestParser()
         self.parser.add_argument('seriesID', type=str, required=True) #----change to accept list 
         self.parser.add_argument('startYear', type=int, required=True)  #-----start year
         self.parser.add_argument('endYear', type=int, required=True)
#                                     -----            format
#     def get(self):
#         return args["seriesID"]    
    def post(self):
        def generate_df(seriesID_list, target_value_name):
            headers = {'Content-type': 'application/json'}
            data = json.dumps({"seriesid": seriesID_list, "startyear":args["startYear"], "endyear":args["endYear"], "registrationkey": registrationkey})
            p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
            if p.status_code == 200:
                target_value = json.loads(p.text)
                seriesID_list = []
                year_list = []
                month_list = []
                target_value_list = []
                for item1 in target_value['Results']['series']:   
                    seriesID = item1['seriesID']
                    for item2 in item1['data']:
                        year = item2['year']
                        month = item2['periodName']
                        target = item2['value']
                        seriesID_list.append(seriesID)
                        year_list.append(year)
                        month_list.append(month)
                        target_value_list.append(target)
                data = {'seriesID': seriesID_list,
                         'year' : year_list,
                         'month': month_list,
                          target_value_name: target_value_list
                         }

                df_tmp = pd.DataFrame(data, columns = ['seriesID', 'year', 'month', target_value_name])  
                df_tmp['state_code'] = df_tmp.apply(lambda x: x.seriesID[3:7], axis = 1)
                return df_tmp
            else:
                return "Fail", p.status_code

        args=self.parser.parse_args()
        slist = args["seriesID"].strip("[").strip("]").replace("\"", "")
        seriesID_list = slist.split(', ')

#06 - labor force
#04 - Unemployment value
#03 - Unemployment rate
#05 - Employment number

        lb_list = []
        uv_list = []
        ur_list = []
        ev_list = []
        for i in seriesID_list:
            if i[-2:] == "06":
                lb_list.append(i)
            if i[-2:] == "05":
                ev_list.append(i)
            if i[-2:] == "04":
                uv_list.append(i)
            if i[-2:] == "03":
                ur_list.append(i)
              
        global df_lb
        global df_uv
        global df_ur
        global df_ev
        
        if len(lb_list) > 0:            
            df_lb = generate_df(lb_list, "labor_force")
        elif len(lb_list) == 0:
            df_lb = pd.DataFrame(columns = ['seriesID', 'year', 'month', 'labor_force', 'state_code'])  
            
        if len(uv_list) > 0:
            df_uv = generate_df(uv_list, "unemployment_value")
        elif len(uv_list) == 0:
            df_uv = pd.DataFrame(columns = ['seriesID', 'year', 'month', 'unemployment_value', 'state_code'])
                    
        if len(ur_list) > 0:
            df_ur = generate_df(ur_list, "unemployment_rate")
        elif len(ur_list) == 0:
            df_ur = pd.DataFrame(columns = ['seriesID', 'year', 'month', 'unemployment_rate', 'state_code'])
                    
        if len(ev_list) > 0:
            df_ev = generate_df(ev_list, "employment_value")
        elif len(ev_list) == 0:
            df_ev = pd.DataFrame(columns = ['seriesID', 'year', 'month', 'employment_value', 'state_code'])         
        
        df_1 = df_lb.merge(df_uv, how = 'outer', on=['year', 'month', 'state_code']).merge(df_ur, how = 'outer', on=['year', 'month', 'state_code']).merge(df_ev, how = 'outer', on=['year', 'month', 'state_code'])

        df_unemployment_index = df_1[["state_code", "year", "month", "labor_force", "employment_value", "unemployment_value", "unemployment_rate"]]
        df_unemployment = df_unemployment_index.to_csv()
        print(df_unemployment)            
        return df_unemployment, 200

########################################################################################
########################################################################################

class get_cpi_data(Resource):
    def __init__ (self):
         self.parser = reqparse.RequestParser()
         self.parser.add_argument('seriesID', type=str, required=True) #----change to accept list 
         self.parser.add_argument('startYear', type=int, required=True)  #-----start year
         self.parser.add_argument('endYear', type=int, required=True)
#                                     -----            format
#     def get(self):
#         return args["seriesID"]    
    def post(self):
        def generate_df(seriesID_list, target_value_name):
            headers = {'Content-type': 'application/json'}
            data = json.dumps({"seriesid": seriesID_list, "startyear":args["startYear"], "endyear":args["endYear"], "registrationkey": registrationkey})
            p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
            if p.status_code == 200:
                target_value = json.loads(p.text)
                seriesID_list = []
                year_list = []
                month_list = []
                target_value_list = []
                for item1 in target_value['Results']['series']:   
                    seriesID = item1['seriesID']
                    for item2 in item1['data']:
                        year = item2['year']
                        month = item2['periodName']
                        target = item2['value']
                        seriesID_list.append(seriesID)
                        year_list.append(year)
                        month_list.append(month)
                        target_value_list.append(target)
                data = {'seriesID': seriesID_list,
                         'year' : year_list,
                         'month': month_list,
                          target_value_name: target_value_list
                         }

                df_tmp = pd.DataFrame(data, columns = ['seriesID', 'year', 'month', target_value_name])  
                df_tmp.head()
                df_tmp['area_code'] = df_tmp.apply(lambda x: x.seriesID[3:8], axis = 1)
                return df_tmp
            else:
                return "Fail", p.status_code

        args=self.parser.parse_args()
        slist = args["seriesID"].strip("[").strip("]").replace("\"", "")
        seriesID_list = slist.split(', ')

# SA0R	Purchasing power of the consumer dollar
# SAS4	Transportation Services
# SAT	Transportation
# SAM	Medical care
# SAS2RS 	Rent of shelter
# SEMF 	Medicinal drugs
# SAF1 	Food
# SAF113 	Fruits and vegetables
# SAF114 	Nonalcoholic beverages and beverage materials
# SAF116 	Alcoholic beverages

        ppcd_list = []
        ts_list = []
        t_list = []
        mc_list = []
        rs_list = []
        md_list = []
        f_list = []
        fv_list = []
        nab_list = []
        ab_list = []
        
        for i in seriesID_list:
            if i[8:] == "SA0R":
                ppcd_list.append(i)
            if i[8:] == "SAS4":
                ts_list.append(i)
            if i[8:] == "SAT":
                t_list.append(i)
            if i[8:] == "SAM":
                mc_list.append(i)
            if i[8:] == "SAS2RS":
                rs_list.append(i)
            if i[8:] == "SEMF":
                md_list.append(i)
            if i[8:] == "SAF1":
                f_list.append(i)
            if i[8:] == "SAF113":
                fv_list.append(i)
            if i[8:] == "SAF114":
                nab_list.append(i)
            if i[8:] == "SAF116":
                ab_list.append(i)
              
        global df_ppcd
        global df_ts
        global df_t
        global df_mc
        global df_rs
        global df_md
        global df_f
        global df_fv
        global df_nab
        global df_ab
        
        
        if len(ppcd_list) > 0:            
            df_ppcd = generate_df(ppcd_list, "Purchasing_power_of_the_consumer_dollar")
        elif len(ppcd_list) == 0:
            df_ppcd = pd.DataFrame(columns = ['seriesID', 'year', 'month', 'Purchasing_power_of_the_consumer_dollar', 'area_code'])  
            
        if len(ts_list) > 0:
            df_ts = generate_df(ts_list, "Transportation_Services")
        elif len(ts_list) == 0:
            df_ts = pd.DataFrame(columns = ['seriesID', 'year', 'month', 'Transportation_Services', 'area_code'])
                    
        if len(t_list) > 0:
            df_t = generate_df(t_list, "Transportation")
        elif len(t_list) == 0:
            df_t = pd.DataFrame(columns = ['seriesID', 'year', 'month', 'Transportation', 'area_code'])
                    
        if len(mc_list) > 0:
            df_mc = generate_df(mc_list, "Medical_care")
        elif len(mc_list) == 0:
            df_mc = pd.DataFrame(columns = ['seriesID', 'year', 'month', 'Medical_care', 'area_code'])
            
        if len(rs_list) > 0:
            df_rs = generate_df(rs_list, "Rent_of_shelter")
        elif len(rs_list) == 0:
            df_rs = pd.DataFrame(columns = ['seriesID', 'year', 'month', 'Rent_of_shelter', 'area_code'])
            
        if len(md_list) > 0:
            df_md = generate_df(md_list, "Medicinal_drugs")
        elif len(md_list) == 0:
            df_md = pd.DataFrame(columns = ['seriesID', 'year', 'month', 'Medicinal_drugs', 'area_code'])
        
        if len(f_list) > 0:
            df_f = generate_df(f_list, "Food")
        elif len(f_list) == 0:
            df_f = pd.DataFrame(columns = ['seriesID', 'year', 'month', 'Food', 'area_code'])
            
        if len(fv_list) > 0:
            df_fv = generate_df(fv_list, "Fruits_and_vegetables")
        elif len(fv_list) == 0:
            df_fv = pd.DataFrame(columns = ['seriesID', 'year', 'month', 'Fruits_and_vegetables', 'area_code'])
        
        if len(nab_list) > 0:
            df_nab = generate_df(nab_list, "Nonalcoholic_beverages_and_beverage_materials")
        elif len(nab_list) == 0:
            df_nab = pd.DataFrame(columns = ['seriesID', 'year', 'month', 'Nonalcoholic_beverages_and_beverage_materials', 'area_code'])
        
        if len(ab_list) > 0:
            df_ab = generate_df(ab_list, "Alcoholic_beverages")
        elif len(ab_list) == 0:
            df_ab = pd.DataFrame(columns = ['seriesID', 'year', 'month', 'Alcoholic_beverages', 'area_code'])
            
            
        
        df_1 = df_ppcd.merge(df_ts, how = 'outer', on=['year', 'month', 'area_code']).merge(df_t, how = 'outer', on=['year', 'month', 'area_code']).merge(df_mc, how = 'outer', on=['year', 'month', 'area_code']).merge(df_rs, how = 'outer', on=['year', 'month', 'area_code']).merge(df_md, how = 'outer', on=['year', 'month', 'area_code']).merge(df_f, how = 'outer', on=['year', 'month', 'area_code']).merge(df_fv, how = 'outer', on=['year', 'month', 'area_code']).merge(df_nab, how = 'outer', on=['year', 'month', 'area_code']).merge(df_ab, how = 'outer', on=['year', 'month', 'area_code'])
        
        df_cpi_index = df_1[["area_code", "year", "month", "Purchasing_power_of_the_consumer_dollar", "Transportation_Services", "Transportation", "Medical_care", "Rent_of_shelter", "Medicinal_drugs", "Food", "Fruits_and_vegetables", "Nonalcoholic_beverages_and_beverage_materials", "Alcoholic_beverages"]]
        df_cpi = df_cpi_index.to_csv()
#        print(df_cpi)            
        return df_cpi, 200
    
#############################################################################################
#############################################################################################




class get_ppi_data(Resource):
    def __init__ (self):
         self.parser = reqparse.RequestParser()
         self.parser.add_argument('seriesID', type=str, required=True) #----change to accept list 
         self.parser.add_argument('startYear', type=int, required=True)  #-----start year
         self.parser.add_argument('endYear', type=int, required=True)
#                                     -----            format
#     def get(self):
#         return args["seriesID"]    
    def post(self):
        def generate_df(seriesID_list, target_value_name):
            headers = {'Content-type': 'application/json'}
            data = json.dumps({"seriesid": seriesID_list, "startyear":args["startYear"], "endyear":args["endYear"], "registrationkey": registrationkey})
            p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
            if p.status_code == 200:
                target_value = json.loads(p.text)
                seriesID_list = []
                year_list = []
                month_list = []
                target_value_list = []
                for item1 in target_value['Results']['series']:   
                    seriesID = item1['seriesID']
                    for item2 in item1['data']:
                        year = item2['year']
                        month = item2['periodName']
                        target = item2['value']
                        seriesID_list.append(seriesID)
                        year_list.append(year)
                        month_list.append(month)
                        target_value_list.append(target)
                data = {'seriesID': seriesID_list,
                         'year' : year_list,
                         'month': month_list,
                          target_value_name: target_value_list
                         }

                df_tmp = pd.DataFrame(data, columns = ['seriesID', 'year', 'month', target_value_name])  
                df_tmp['area_code'] = df_tmp.apply(lambda x: x.seriesID[-1], axis = 1)
                df_tmp['type'] = df_tmp.apply(lambda x: x.seriesID[-2], axis = 1)
                return df_tmp
            else:
                return "Fail", p.status_code

        args=self.parser.parse_args()
        slist = args["seriesID"].strip("[").strip("]").replace("\"", "")
        seriesID_list = slist.split(', ')

##PCU
#####PCU - 2211222211224 - 1 - 1
#####PCU - 22121022121011

##   electric power 221122
##   residential  2211224 - 11 (New England)
##   commercial   2211224 - 21 (New England)
##   industrial   2211224 - 31 (New England)
##                2211224 - 12 (other area)

##   natural gas  221210
##   residential  22121011 - 21 (New England)
##   commercial   22121011 - 31 (New England)
##   industrial   22121011 - 41 (New England)


        electric_list = []
        natural_gas_list = []
        for i in seriesID_list:
            if i[3:16] == "2211222211224":
                electric_list.append(i)
            if i[3:17] == "22121022121011":
                natural_gas_list.append(i)
              
        global df_electric
        global df_natural_gas
        
        if len(electric_list) > 0:            
            df_electric = generate_df(electric_list, "electric_power")
        elif len(electric_list) == 0:
            df_electric = pd.DataFrame(columns = ['seriesID', 'year', 'month', 'electric_power', 'area_code', 'type'])  
            
        if len(natural_gas_list) > 0:
            df_natural_gas = generate_df(natural_gas_list, "natural_gas")
        elif len(natural_gas_list) == 0:
            df_natural_gas = pd.DataFrame(columns = ['seriesID', 'year', 'month', 'natural_gas', 'area_code', 'type'])
                    
        df_1 = df_electric.merge(df_natural_gas, how = 'outer', on=['year', 'month', 'area_code'])
        df_ppi_index = df_1[["area_code", "year", "month", "electric_power", "natural_gas", "type_x", "type_y"]]
        df_ppi_index.rename(columns = {'type_x': 'electric_power_type_num', 'type_y': 'natural_gas_type_num'}, inplace = True) 
        
# event_dictionary ={'Music' : 1500, 'Poetry' : 800, 'Comedy' : 1200} 
  
# # Add a new column named 'Price' 
# df['Price'] = df['Event'].map(event_dictionary) 

        elec_dic = {'1' : 'residential', '2' : 'commercial', '3' : 'industrial', '': None}
        natural_dic = {'2' : 'residential', '3' : 'commercial', '4' : 'industrial', '': None}
        df_ppi_index['electric_power_type'] = df_ppi_index['electric_power_type_num'].map(elec_dic)
        df_ppi_index['natural_gas_type'] = df_ppi_index['natural_gas_type_num'].map(natural_dic)
        df_ppi_index_new = df_ppi_index[["area_code", "year", "month", "electric_power", "natural_gas", "electric_power_type_num", "natural_gas_type_num"]]
        df_ppi = df_ppi_index.to_csv()
        print(df_ppi)

        
        return df_ppi, 200
    
    
    
api.add_resource(get_ui_data, '/ui')
api.add_resource(get_cpi_data, '/cpi')
api.add_resource(get_ppi_data, '/ppi')

if __name__ == '__main__':

#    APP.run(host='0.0.0.0')
    app.run()


# In[ ]:




