import pandas as pd
import unitsmod
import inspect
import time
import os 

path = inspect.getabsfile(unitsmod).replace('__init__.py', '')
database = pd.read_excel(path+'database.xlsx')

unitTypes = []
for header in database.columns:
    if header.find('Unit') != -1 and header.find('%') == -1:
        unitTypes.append(header.replace('Unit',''))

def editDataBase():
    os.startfile(path)
    return "DataBase is opening in your Excel, please wait. This task can take some time. It depends of yours operational system."

def consutDataBase():
    pathToDocumentation = path+'documentation\\databasetables.html'

    with open(pathToDocumentation, 'r') as f:  # Loads the content  
        htmlFile = f.read()

    htmlBegin = htmlFile[:htmlFile.find('</section>')+len('</section>\n')]
    htmlEnd = htmlFile[htmlFile.find('</body>'):]

    update = "\t\t<select id='unitSelector'>\n"
    
    for item in unitTypes:
        update = update + "\t\t\t<option value='{}'>{}</option>\n".format(item, item)
    update = htmlBegin + update + "\t\t</select>\n"

    for item in unitTypes: 
        table = database.loc[:,['{}Unit'.format(item),'{}Conv'.format(item)]].dropna(0)
        table.columns = ['Unit', 'Conversion Factor']
        table =  table.to_html(table_id = '{}'.format(item),border=0, justify='right',index=False)
        update = update + "\t\t<div id='{}' class='begin'>\n\t\t\t".format(item+'div') + table + '\n\t\t</div>\n'
    update = update + htmlEnd

    with open(pathToDocumentation, 'w') as f:
            f.write(update)

    print ("DataBase is opening in your Browser, please wait.")
    print("This task may take some time. It depends of your operational system.")
    time.sleep(2)
    os.startfile(pathToDocumentation)