from unitsmod import database as dt
from unitsmod.dimensionClass import dimension as dm

def compareType(unitFrom, unitTo):
    for item in unitFrom:
        same = False
        for term in unitTo:
            if(item == term):
                same = True
        if not same:
            return False
    return True

def conv(unitFrom, unitTo):
    unitFrom = dm(unitFrom)
    unitTo = dm(unitTo)
    if(compareType(unitFrom.type, unitTo.type)):
        return unitFrom.convertConstant/unitTo.convertConstant
    else:
        message = 'thermo.py: {} and {} are not dimensionally similar'
        print(message.format(unitFrom.dType(), unitTo.dType()))
        return 0

def convTemp(temp, unitFrom, unitTo):
    convConst = [[unitFrom], [unitTo]]
    for unit in convConst:
        container = dt.database.loc[dt.database['%temperatureUnit']== unit[0]][['temperatureIntervalConv', '%temperatureConv']].values[0]
        unit.append(container[0])
        unit.append(container[1])
    return (temp-convConst[0][2])*(convConst[0][1]/convConst[1][1])+convConst[1][2]