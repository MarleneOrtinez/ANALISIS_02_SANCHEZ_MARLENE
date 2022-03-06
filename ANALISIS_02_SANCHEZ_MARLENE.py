#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import pandas as pd

base = pd.read_csv("/Users/Monse/Downloads/synergy_logistics_database.csv")


"""
1.Synergy logistics está considerando la posibilidad de enfocar sus esfuerzos en las 10 rutas más demandadas.
Acorde a los flujos de importación y exportación, ¿cuáles son esas 10 rutas?
"""

top_rutas = base.groupby(['origin','destination'])
suma = top_rutas.sum()['total_value']
top_rutas =top_rutas.count()['register_id'].sort_values(ascending=False)
top_rutas=pd.DataFrame(top_rutas)
top_rutas['contributed money'] = suma
top_rutas= top_rutas.reset_index()
top_rutas=top_rutas.head(10)
top_rutas=top_rutas.rename(columns= {'register_id': 'times used'})
print(top_rutas)


sum_top_rutas = top_rutas.sum()['contributed money']
sum_total= base.sum()['total_value']
porcent = (sum_top_rutas/sum_total)*100
print(f'Las rutas mas demandadas aportan ${sum_top_rutas}, es decir {porcent}% de las ganancias totales')

sum_times_used = top_rutas.sum()['times used']
total_times_used=base.count()['register_id']
print(f'Las rutas más demandadas se usaron {sum_times_used} veces de un total de {total_times_used}')


"""
2. ¿Cuáles son los 3 medios de transporte más importantes para Synergy logistics considerando el valor de las importaciones y exportaciones?
"""

transport= base.groupby('transport_mode')
transport = transport.sum()['total_value'].sort_values(ascending=False)
transport= transport.reset_index()
transport = transport.rename(columns={'total_value':'money_contributed'})
transport['percentage_contributed'] = transport['money_contributed']/transport['money_contributed'].sum()*100
print(transport)

"""
3. Si Synergy Logistics quisiera enfocarse en los países que le generan el 80% del valor de las exportaciones e importaciones ¿en qué grupo de países debería enfocar sus esfuerzos?
"""

imports = base[base['direction']== 'Imports']
exports = base[base['direction']== 'Exports']


rutas_exp = exports.groupby(['origin'])
rutas_imp = imports.groupby(['origin'])
rutas = base.groupby(['origin'])


rutas_exp = rutas_exp.sum()['total_value'].sort_values(ascending=False)
rutas_exp = rutas_exp.reset_index()
#rutas_exp
rutas_imp = rutas_imp.sum()['total_value'].sort_values(ascending=False)
rutas_imp = rutas_imp.reset_index()
#rutas_imp
rutas = rutas.sum()['total_value'].sort_values(ascending=False)
rutas = rutas.reset_index()
#rutas



rutas_exp['contribution'] = rutas_exp['total_value']/rutas_exp['total_value'].sum()*100
rutas_exp['contribution_acum'] = rutas_exp.cumsum()['contribution']
#rutas_exp
rutas_imp['contribution'] = rutas_imp['total_value']/rutas_imp['total_value'].sum()*100
rutas_imp['contribution_acum'] = rutas_imp.cumsum()['contribution']
#rutas_imp
rutas['contribution'] =rutas['total_value']/rutas['total_value'].sum()*100
rutas['contribution_acum']=rutas.cumsum()['contribution']
#rutas


top_rutas_exp = rutas_exp[rutas_exp['contribution_acum']<=85]
print(top_rutas_exp)


top_rutas_imp= rutas_imp[rutas_imp['contribution_acum']<=85]
print(top_rutas_imp)


top_rutas =rutas[rutas['contribution_acum']<=82]
print(top_rutas)

