# -*- coding: utf-8 -*-
"""Heart Disease _sri

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14ffJAXtx2aigscaFu8Zi_5eA-QBWl4tu
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
import keras
from keras.models import Sequential
from keras.layers import Dense
import warnings

from google.colab import drive 
drive.mount('/content/gdrive')

import pandas as pd 
df=pd.read_csv('gdrive/My Drive/Heart.csv')

df.head()

"""Cleaveland database.

1. Hungarian Institute of Cardiology. Budapest.
2. University Hospital, Zurich, Switzerland.
3. University Hospital, Basel, Switzerland.
4. V.A. Medical Center, Long Beach and Cleveland Clinic Foundation.

Our Data contains:

   1. age - age in years
   2. sex - (1 = male; 0 = female)
   3. cp - chest pain type    // categorical values.
        0: Typical angina: chest pain related decrease blood supply to the heart
        1: Atypical angina: chest pain not related to heart
        2: Non-anginal pain: typically esophageal spasms (non heart related)
        3: Asymptomatic: chest pain not showing signs of disease
   4. trestbps - resting blood pressure (in mm Hg on admission to the hospital) anything above 130-140 is typically cause for concern
   5. chol - serum cholestoral in mg/dl
            serum = LDL + HDL + .2 * triglycerides
            above 200 is cause for concern
   6. fbs - (fasting blood sugar > 120 mg/dl) (1 = true; 0 = false)
            '>126' mg/dL signals diabetes
   7. restecg - resting electrocardiographic results   // categorical values.
        0: Nothing to note
        1: ST-T Wave abnormality
            can range from mild symptoms to severe problems
            signals non-normal heart beat
        2: Possible or definite left ventricular hypertrophy
            Enlarged heart's main pumping chamber
   8. thalach - maximum heart rate achieved   
   9. exang - exercise induced angina (1 = yes; 0 = no)
   
  10. oldpeak - ST depression induced by exercise relative to rest looks at stress of heart during excercise unhealthy heart will stress more
  11. slope - the slope of the peak exercise ST segment    // categorical values.
        0: Upsloping: better heart rate with excercise (uncommon)
        1: Flatsloping: minimal change (typical healthy heart)
        2: Downslopins: signs of unhealthy heart   
  12. ca - number of major vessels (0-3) colored by flourosopy    // categorical values.
        colored vessel means the doctor can see the blood passing through
        the more blood movement the better (no clots)
  13. thal - thalium stress result    // categorical values. 
        1,3: normal
        6: fixed defect: used to be defect but ok now
        7: reversable defect: no proper blood movement when excercising
  14. target - have disease or not (1=yes, 0=no) (= the predicted attribute)
"""

df.target.value_counts()

noofpatientshavingdisease=len(df[df.target==1])
noofpatientsnothavingdisease=len(df[df.target==0])
totalpatients=len(df.target)
print("percentage of patients suffering from heart disease: {:.4f}%".format((noofpatientshavingdisease/totalpatients)*100))
print("percentage of patients not suffering from heart disease: {:.4f}%".format((noofpatientsnothavingdisease/totalpatients)*100))

sns.countplot(x="sex",data=df)
plt.xlabel("0=female,1=male")
plt.show()

pd.crosstab(df.sex,df.target).plot(kind="bar",figsize=(10,5))
plt.title('Heart Disease Frequency for Sex')
plt.xlabel('Sex (0 = Female, 1 = Male)')
plt.legend(["Not having Disease", "Having Disease"])
plt.ylabel('Frequency with respect to Sex')
plt.xticks(rotation=0)
plt.show()

pd.crosstab(df.age,df.target).plot(kind="bar",figsize=(20,5))
plt.title("Heart Disease frequency for ages")
plt.xlabel("Ages")
plt.legend(["Not having Disease", "Having Disease"])
plt.ylabel("Frequency with respect to ages")
plt.show()

#thalach : (here maximum heart rate)
plt.scatter(x=df.age[df.target==1], y=df.thalach[(df.target==1)], c="red")
plt.scatter(x=df.age[df.target==0], y=df.thalach[(df.target==0)])
plt.legend(["Disease", "Not Disease"])
plt.xlabel("Age")
plt.ylabel("Maximum Heart Rate")
plt.show()

pd.crosstab(df.fbs,df.target).plot(kind="bar",figsize=(15,6))
plt.title('Heart Disease Frequency According To FBS')
plt.xlabel('FBS > 120 mg/dl (0 = False, 1 = True)')
plt.legend(["Not having Disease", "Having Disease"])
plt.ylabel('Frequency with respect to FBS')
plt.xticks(rotation=0)
plt.show()

#trestbps(blood pressure)
pd.crosstab(df.trestbps,df.target).plot(kind="bar",figsize=(20,8))
plt.title('Heart disease according to Blood Pressure')
plt.xlabel('Blood pressure')
plt.xticks(rotation=0)
plt.legend(["Not having Disease", "Having Disease"])
plt.ylabel('Frequency with respect to Blood Pressure')
plt.show()

pd.crosstab(df.restecg,df.target).plot(kind="bar",figsize=(15,6))
plt.title('Heart Disease Frequency According To restecg')
plt.xlabel('restecg - resting electrocardiographic results ,(0-2)' )
plt.xticks(rotation = 0)
plt.legend(["Not having Disease", "Having Disease"])
plt.ylabel('Frequency with repect to restecg')
plt.show()

pd.crosstab(df.cp,df.target).plot(kind="bar",figsize=(15,5))
plt.title('Heart Disease Frequency According To Chest Pain Type')
plt.xlabel('Chest Pain Type ,(0-3)')
plt.xticks(rotation = 0)
plt.ylabel('Frequency with respect to cp')
plt.show()

a= pd.get_dummies(df['cp'],prefix="cp")
b= pd.get_dummies(df['restecg'],prefix="restecg")
c= pd.get_dummies(df['slope'],prefix="slope")
d= pd.get_dummies(df['thal'],prefix="thal")
e= pd.get_dummies(df['ca'],prefix="ca")

frames=[df,a,b,c,d,e]
df=pd.concat(frames,axis=1)
df.head()

df = df.drop(columns=['cp','restecg' , 'slope','thal','ca'])
df.head()

y = df.target.values
x_data = df.drop(['target'], axis = 1)

x = (x_data - np.min(x_data)) / (np.max(x_data) - np.min(x_data)).values

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.25,random_state=0)

print("Train feature shape" ,x_train.shape)
print("Test feature shape" , x_test.shape)

accuracies_model={}

#Logistic Regression
from sklearn.linear_model import LogisticRegression

lr = LogisticRegression()
lr.fit(x_train,y_train)
acc = lr.score(x_test,y_test)*100

accuracies_model['Logistic Regression']=acc
print("Test Accuracy of Logistic Regression Algorithm {:.4f}%".format(acc))

# Support Vector Machine
from sklearn.svm import SVC
svm = SVC(random_state = 1)
svm.fit(x_train, y_train)

acc = svm.score(x_test,y_test)*100
accuracies_model['Support Vector Machine']=acc
print("Test Accuracy of Support Vector Machine Algorithm: {:.4f}%".format(acc))

# K-nearest Neighbors
from sklearn.neighbors import KNeighborsClassifier
X=[]
for i in range(1,20):
    knn=KNeighborsClassifier(n_neighbors=i)
    knn.fit(x_train,y_train)
    X.append(knn.score(x_test,y_test))
    
plt.plot(range(1,20),X)
plt.xlabel("K-number")
plt.ylabel("Score")
plt.show()

bestScore=max(X)*100
print("K-nearest Neighbors Accuracy =",format(bestScore))
accuracies_model['K-nearest Neighbors']=bestScore

#Random forest 
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators = 3000, random_state = 1)
rf.fit(x_train, y_train)

acc = rf.score(x_test,y_test)*100
accuracies_model['Random Forest']=acc
print("Random Forest Algorithm Accuracy Score : {:.2f}%".format(acc))

def NN_model(learning_rate):
    model = Sequential()
    model.add(Dense(32, input_dim=27, kernel_initializer='normal', activation='relu'))
    model.add(Dense(16, kernel_initializer='normal', activation='relu'))
    model.add(Dense(2, activation='softmax'))
    Adam(lr=learning_rate)
    model.compile(loss='sparse_categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])
    return model

learning_rate = 0.01
model = NN_model(learning_rate)
print(model.summary())

history = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=100, batch_size=16, verbose=2)

# Plot the model accuracy vs. number of Epochs
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epochs')
plt.legend(['Train', 'Test'])
plt.show()

# Plot the Loss function vs. number of Epochs
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epochs')
plt.legend(['Train', 'Test'])
plt.show()

from sklearn.metrics import  accuracy_score
predictions = np.argmax(model.predict(x_test), axis=1)
model_accuracy = accuracy_score(y_test, predictions)*100
accuracies_model['neural network']=model_accuracy
print("Model Accuracy:", model_accuracy,"%")

plt.figure(figsize=(12,5))
plt.ylabel("Accuracy %")
plt.xlabel("Algorithms")
sns.barplot(x=list(accuracies_model.keys()), y=list(accuracies_model.values()))
plt.show()

y_head_lr = lr.predict(x_test)
y_head_svm=svm.predict(x_test)
knn2=KNeighborsClassifier(n_neighbors=6)
knn2.fit(x_train,y_train)

y_head_knn=knn2.predict(x_test)

y_head_rf=rf.predict(x_test)

from sklearn.metrics import confusion_matrix

cm_lr = confusion_matrix(y_test,y_head_lr)
cm_svm = confusion_matrix(y_test,y_head_svm)
cm_knn = confusion_matrix(y_test,y_head_knn)
cm_rf =  confusion_matrix(y_test,y_head_rf)
cm_neural = confusion_matrix(y_test,predictions)

plt.figure(figsize=(14,18))

plt.suptitle("Confusion Matrixes",fontsize=25)


plt.subplot(3,2,1)
plt.title("Logistic Regression Confusion Matrix")
sns.heatmap(cm_lr,annot=True,cmap="summer",fmt="d",cbar=False, annot_kws={"size": 24})


plt.subplot(3,2,2)
plt.title("Support Vector Machine Confusion Matrix")
sns.heatmap(cm_svm,annot=True,cmap="summer",fmt="d",cbar=False, annot_kws={"size": 24})

plt.subplot(3,2,3)
plt.title("K-nearest Neighbors Confusion Matrix")
sns.heatmap(cm_knn,annot=True,cmap="summer",fmt="d",cbar=False, annot_kws={"size": 24})

plt.subplot(3,2,4)
plt.title("Random Forest Confusion Matrix")
sns.heatmap(cm_rf,annot=True,cmap="summer",fmt="d",cbar=False, annot_kws={"size": 24})

plt.subplot(3,2,5)
plt.title("neural network Confusion Matrix")
sns.heatmap(cm_neural,annot=True,cmap="summer",fmt="d",cbar=False, annot_kws={"size": 24})