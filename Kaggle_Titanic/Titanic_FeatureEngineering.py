#---- Import Package ----
import numpy as np
import pandas as pd

#---- Call Azure ML ----
def azureml_main(dataframe1):
    
    data_final = dataframe1
    
    #-- Passenger Name --
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
    data_final['Title'] = data_final['Name'].map(lambda name:name.split(',')[1].split('.')[0].strip())
    # Mapping new Title
    data_final['Title'] = data_final.Title.map(Title_Dictionary)
    # Encoding in dummy variable
    dummy_title = pd.get_dummies(data_final['Title'], prefix='Title')
    data_final = pd.concat([data_final, dummy_title], axis=1)
    
    #-- Passenger Age -- 
    grouped_data = data_final.groupby(['Sex','Pclass','Title'])
    grouped_data_median = grouped_data.median()
    grouped_data_median = grouped_data_median.reset_index()[['Sex', 'Pclass', 'Title', 'Age']]
    
    def fill_age(data):
        fill_id = ( (grouped_data_median['Sex'] == data['Sex']) & 
                   (grouped_data_median['Title'] == data['Title']) & 
                   (grouped_data_median['Pclass'] == data['Pclass']) )
        return grouped_data_median[fill_id]['Age'].values[0]
    
    data_final['Age'] = data_final.apply(lambda data: fill_age(data) if np.isnan(data['Age']) else data['Age'], axis=1)
    
    #-- Fare -- 
    data_final.Fare.fillna(data_final.Fare.mean(), inplace=True)
    
    #-- Embarked -- 
    data_final.Embarked.fillna('S', inplace=True)
    # Encoding in dummy variable
    dummy_embarked = pd.get_dummies(data_final['Embarked'], prefix='Embarked')
    data_final = pd.concat([data_final, dummy_embarked], axis=1)
    
    #-- Cabin -- 
    # Missing : M
    data_final.Cabin.fillna('M', inplace=True)
    # Get Each Cabin First letter
    data_final['Cabin'] = data_final['Cabin'].map(lambda l: l[0])
    # Encoding in dummy variable
    dummy_cabin = pd.get_dummies(data_final['Cabin'], prefix='Cabin')
    data_final = pd.concat([data_final, dummy_cabin], axis=1)
    
    #-- Sex -- 
    data_final['Sex'] = data_final['Sex'].map({'male':1, 'female':0})
    
    #-- Pclass -- 
    # Encoding in dummy variable
    dummy_pclass = pd.get_dummies(data_final['Pclass'], prefix='Pclass')
    data_final = pd.concat([data_final, dummy_pclass], axis=1)
    
    #-- Ticket -- 
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
        
    data_final['Ticket'] = data_final['Ticket'].map(cleanTicket)
    # Encoding in dummy variable
    dummy_tickets = pd.get_dummies(data_final['Ticket'], prefix='Ticket')
    data_final = pd.concat([data_final, dummy_tickets], axis=1)
    
    #-- Family -- 
    data_final['Family_size'] = data_final['Parch'] + data_final['SibSp'] + 1
    # Introducing other features based on the family size
    data_final['Single_family'] = data_final['Family_size'].map(lambda s: 1 if s == 1 else 0)
    data_final['Small_family'] = data_final['Family_size'].map(lambda s: 1 if 2 <= s <= 4 else 0)
    data_final['Big_family'] = data_final['Family_size'].map(lambda s: 1 if 5 <= s else 0)
    
    #-- Drop some columns since we won't be using it anymore -- 
    data_final.drop(['PassengerId','Name','Title','Embarked','Cabin','Pclass','Ticket'], axis=1, inplace=True)
    
    result = data_final
    
    return result,