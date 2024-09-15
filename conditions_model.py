import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from mappings import weather_mappings,direction_mapping
df=pd.read_csv('delhirain.csv')

#Data Preprocessing
df.columns  = df.columns.str.lstrip(' _')
df = df.drop(columns = ['precipm','wgustm','windchillm','heatindexm','rain','snow','hail','tornado','thunder']) # Feature extraction
df = df.drop(columns = ['wdird'])
df = df.dropna()#Null values handling

#Feature engineering
df['wdire'] = df['wdire'].map(direction_mapping)
df = df.drop(columns = 'datetime_utc')
df = df[df['conds'] != 'Unknown']
df['conds']=df['conds'].map(weather_mappings)

#Train Test Split
X = df.drop(columns = ['conds'])
y = df['conds']
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)

#Label encoding 
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_train = le.fit_transform(y_train)
#Model Selection
from xgboost import XGBClassifier;
model = XGBClassifier(n_estimators=200, learning_rate=0.1,n_jobs = -1,max_depth = 9,random_state = 42)
model.fit(X_train, y_train,
             verbose=False)

pickle.dump(model,open("conditions_model.pkl","wb"))