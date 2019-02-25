#---- Import Package ----
import numpy as np
import pandas as pd

#---- Call Azure ML ----
def azureml_main(dataframe1):
    
    input_data = dataframe1
    
    #----- Passenger Name -----
    Title_Dictionary = {
        "Capt": "Officer",
        "Col": "Officer",
        "Major": "Officer",
        "Jonkheer": "Royalty",
        "Don": "Royalty",
        "Dona": "Royalty",
        "Sir" : "Royalty",
        "Dr": "Officer",
        "Rev": "Officer",
        "the Countess":"Royalty",
        "Mme": "Mrs",
        "Mlle": "Miss",
        "Ms": "Mrs",
        "Mr" : "Mr",
        "Mrs" : "Mrs",
        "Miss" : "Miss",
        "Master" : "Master",
        "Lady" : "Royalty"
    }
    # Split Name
    input_data['Title'] = input_data['Name'].map(lambda name:name.split(',')[1].split('.')[0].strip())
    # Mapping new Title
    input_data['Title'] = input_data.Title.map(Title_Dictionary)
    # Encoding in dummy variable
    dummy_title = pd.get_dummies(input_data['Title'], prefix='Title')
    input_data = pd.concat([input_data, dummy_title], axis=1)
    #--------------------

    #----- Passenger Age -----
    fill_age_grouped = {'Sex': ['female','female','female','female','female','female','female','female',
                                'male','male','male','male','male','male','male','male','male'],
                        'Pclass': [1,1,1,1,2,2,3,3,1,1,1,1,2,2,3,3,3],
                        'Title': ['Miss','Mrs','Officer','Royalty','Miss','Mrs','Miss','Mrs','Master',
                                  'Mr','Officer','Royalty','Master','Mr','Officer','Master','Mr'],
                        'Age': [30.0,40.0,49.0,40.5,24.0,31.5,18.0,31.0,4.0,40.0,51.0,40.0,1.0,31.0,46.0,4.0,26.0]}
    fill_age_grouped = pd.DataFrame.from_dict(fill_age_grouped)
    # Fill Function
    def fill_age(data):
        fill_id = ( (fill_age_grouped['Sex'] == data['Sex']) & 
                    (fill_age_grouped['Title'] == data['Title']) & 
                   (fill_age_grouped['Pclass'] == data['Pclass']) )
        return fill_age_grouped[fill_id]['Age'].values[0]
    # Fill Data
    input_data['Age'] = input_data.apply(lambda data: fill_age(data)
                                                      if np.isnan(data['Age']) else data['Age'], axis=1)
    #--------------------

    #----- Fare -----
    fill_fare = 32.20
    # Fill Data
    input_data.Fare.fillna(fill_fare, inplace=True)
    #--------------------

    #----- Embarked -----
    fill_embarked = 'S'
    # Fill Data
    input_data.Embarked.fillna('S', inplace=True)
    # Encoding in dummy variable
    dummy_embarked = pd.get_dummies(input_data['Embarked'], prefix='Embarked')
    input_data = pd.concat([input_data, dummy_embarked], axis=1)
    #--------------------
    
    #----- Cabin -----
    # Fill Data
    input_data.Cabin.fillna('M', inplace=True)
    # Get Each Cabin First letter
    input_data['Cabin'] = input_data['Cabin'].map(lambda l: l[0])
    # Encoding in dummy variable
    dummy_cabin = pd.get_dummies(input_data['Cabin'], prefix='Cabin')
    input_data = pd.concat([input_data, dummy_cabin], axis=1)
    #--------------------

    #----- Sex -----
    input_data['Sex'] = input_data['Sex'].map({'male':1, 'female':0})
    #--------------------
    
    #----- Pclass -----
    # Encoding in dummy variable
    dummy_pclass = pd.get_dummies(input_data['Pclass'], prefix='Pclass')
    input_data = pd.concat([input_data, dummy_pclass], axis=1)
    #--------------------
    
    #----- Ticket -----
    # Clean Function    
    def cleanTicket(ticket):
        ticket = ticket.replace('.', '')
        ticket = ticket.replace('/', '')
        ticket = ticket.split()
        ticket = map(lambda t : t.strip(), ticket)
        ticket = list(filter(lambda t : not t.isdigit(), ticket))
        if len(ticket) > 0:
            return ticket[0]
        else: 
            return 'Null'
    # Clean Data
    input_data['Ticket'] = input_data['Ticket'].map(cleanTicket)
    # Encoding in dummy variable
    dummy_tickets = pd.get_dummies(input_data['Ticket'], prefix='Ticket')
    input_data = pd.concat([input_data, dummy_tickets], axis=1)
    #--------------------
    
    #----- Family -----
    input_data['Family_size'] = input_data['Parch'] + input_data['SibSp'] + 1
    # Introducing other features based on the family size
    input_data['Single_family'] = input_data['Family_size'].map(lambda s: 1 if s == 1 else 0)
    input_data['Small_family'] = input_data['Family_size'].map(lambda s: 1 if 2 <= s <= 4 else 0)
    input_data['Big_family'] = input_data['Family_size'].map(lambda s: 1 if 5 <= s else 0)
    #--------------------
    
    return input_data,
