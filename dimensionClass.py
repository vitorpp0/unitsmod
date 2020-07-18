import unitsmod.database as dt

class dimension:
    """
        Description
        -----------
        This class holds every aspect of a unit of measure and translate it from a string 
        of speaked language to an array that can be easely used by any function or 
        automated routine. 

        Parameters
        ----------
            unit_measure: string
                This parameter must be a string of a math expression of the units of measure like 'kg*m^2/s^2'.
                The units of measure that can be used are defined in the database.xlsx.
                You can change the unit's names or add new ones by calling the function editDataBase().

                Attention: The units are not case sensitive!

                The operations allowed are: 
                    - '/' : 
                        Interpreted as division, can only appear once.
                        Others '/' in the string will be interpreted 
                        as units of measures not defined in database. 

                    - '*': 
                        Interpreted as products between units of measures. 
                        Works as the * python's math operator.

                    - '^':
                        Interpreted as power operator, works as the ** python's operator.
                        It's accept floats separated by '.'.

                Examples:
                ---------
                    import thermo as tm  
                
                    # Initializing a energy unit object 

                    >>> objectName = tm.unit('kg*m^2/s^2')
                    >>> objectName.type
                    'mass^1.0*distance^2.0*temporal^-2.0'
                    ----------------------------------------------------
                    # Another way to initialize the same unit of measure

                    >>> objectName1 = tm.unit('kg*m^2*s^-2')
                    >>> objectName1.type
                    'mass^1.0*distance^2.0*temporal^-2.0'
                    ----------------------------------------------------
                    # No case sensitive demonstration

                    >>> objectName2 = tm.unit('Kg*M^2*s^-2')
                    >>> objectName2.type
                    'mass^1.0*distance^2.0*temporal^-2.0'
                    ----------------------------------------------------
                    # Not defined units:

                    >>> objectName3 = tm.unit('vitor*j/mi')
                    thermo.py: vitor is not registered in yours database.
                    ----------------------------------------------------
                     # Empty strings:
                    >>> objectName4 = tm.unit('mi*j/')
                    thermo.py:  is not registered in yours database.

                    # As you can see, betwen / there is the joule unit and empty string 
                    # Which is interpreted as a unit measure not defined in the database
                    ----------------------------------------------------
                    # Powered by invalid strings:

                    >>> objectName5 = tm.unit('mi^87k/month')
                    thermo.py: Error in mi^87k, the power operator only works with numbers.

        Properties
        ----------
        The unit of measure class has 3 properties:
            - value: 
                Returns the string typed in the initialization
            
            - info: 
                Returns an multdimension array with all the informations about each unit in .value
                Each .info's line has the following structer:
                    [
                        unit of measure, 
                            A string with a unit of measure recognized in the database
                        power degree,
                            The float with which the unit of measure is powered
                        type,
                            String with unit of measure's type reconized in the database
                        convertion constant to S.I.
                            The float that converts the unit of measure to the I.S 
                    ]
                The convertion constant actually converts the unit of measure to 
                the unit in it's type column in the database.xlsx
            
            - type: 
                A string containing the unit object's type

            Example
            -------
                import thermo as tm
                >>> objectName = tm.unit('mi^87/month')
                >>> objectName.value
                'mi^87/month'
                >>> objectName.info
                [['mi', 87.0, 'distance', 1609.34], ['month', 1.0, 'temporal', 2592000.0]]
                >>> objectName.type
                'distance^87.0*temporal^1.0'
            
            Realize that in the .info example:
                The constant 1609.34 converts 1 mile(mi) to meters(m) and
                the contant 2592000.0 converts 1 month to second(s).
    """
    def __init__(self, measure_unit):
        """
            Parameters
            ----------
                As described above, receives an external parameter measure_unit which is a string
            
            Properties
            ----------
                As described above, initialize the properties: 
                    - .value
                    -.info
                    -.type

            Private
            -------
                Calls the private function __start(self) that manage the object's 
                build with others private functions:
                - __findExpressionTerms(self)
                    Recognize the individuals units in .value
                    and upload the first two items in each .info's line.

                - __completeInfo(self)
                    Access the the database to recognize each individual units type.
                    Also upload the finals 2 items in each .info's line. 

                - __defineType
                    Use the .info propertie to update the .type propertie value. 
        """
        self.value = measure_unit.lower()
        self.info = []
        self.type = []
        self.convertConstant = 1
        
        # Fill the object's parameters 
        self.__start() 

    # Build-in private functions

    def __start(self):
        go, message = self.__findExpressionTerms()
        if go: 
            go, message = self.__completeInfo()
            if go:
                self.__defineType()
                self.__defineTotalCovertConstant()
            else:
                print(message)
        else: print(message)
    
    def __findExpressionTerms(self):
        count, units, detail = 0, [], []
        for position in self.value.split('/', 1):
            for term in position.split('*'):
                if term.find('^') != -1:
                    try: 
                        detail.append([ term.split('^')[0] , float(term.split('^')[1])*((-1)**count) ])
                        units.append(term.split('^')[0])
                    except(ValueError):
                        return False, "dimensionClass.py: Error with {}, the ^ operator must receive a number.".format(term)
                else: 
                    detail.append([term, (-1)**count])
                    units.append(term)
            count+=1
        units = list(dict.fromkeys(units))
        for unit in units:
            power = 0
            for item in detail:
                if(unit == item[0]):
                    power+=item[1]
            self.info.append([unit, power])    
        return True, ''

    def __completeInfo(self):
        for item in self.info:
            notFinded = True
            for tp in dt.unitTypes:
                dataline = dt.database.loc[ dt.database[tp+'Unit'] == item[0] ]
                if not dataline.empty:
                    notFinded = False
                    item.append(tp)
                    item.append(dataline[tp + 'Conv'].values[0])
            if notFinded:
                return False, "dimensionClass.py: {} is not registered in yours database.".format(item[0])
        return True,''
    
    def __defineType(self):
        types = []
        for item in self.info:
            types.append(item[2])
        types = list(dict.fromkeys(types))
        for tp in types:
            power = 0
            for item in self.info:
                if(tp == item[2]):
                    power+=item[1]
            self.type.append([tp, power])
    
    def __defineTotalCovertConstant(self):
        for term in self.info:
            self.convertConstant = self.convertConstant*pow(term[3], term[1])

    def dType(self):
        response = ''
        for item in self.type:
            response = response + '*{}^{}'.format(item[0], item[1])
        response = response.replace('*','',1)
        return response 
