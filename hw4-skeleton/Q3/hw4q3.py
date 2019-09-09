## Data and Visual Analytics - Homework 4
## Georgia Institute of Technology
## Applying ML algorithms to detect eye state

import numpy as np
import pandas as pd
import time

from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA

######################################### Reading and Splitting the Data ###############################################
# XXX
# TODO: Read in all the data. Replace the 'xxx' with the path to the data set.
# XXX
data = pd.read_csv('eeg_dataset.csv')

# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data.
random_state = 100

# XXX
# TODO: Split 70% of the data into training and 30% into test sets. Call them x_train, x_test, y_train and y_test.
# Use the train_test_split method in sklearn with the parameter 'shuffle' set to true and the 'random_state' set to 100.
# XXX

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, shuffle = True, test_size = 0.3, random_state = 100)


# ############################################### Linear Regression ###################################################
# XXX
# TODO: Create a LinearRegression classifier and train it.
# XXX

#Create model
regr = LinearRegression()
#Train model
regr.fit(x_train, y_train)

# XXX
# TODO: Test its accuracy (on the training set) using the accuracy_score method.
# TODO: Test its accuracy (on the testing set) using the accuracy_score method.
# Note: Round the output values greater than or equal to 0.5 to 1 and those less than 0.5 to 0. You can use y_predict.round() or any other method.
# XXX



#Test accuracy on training set
y_pred_train=regr.predict(x_train)
print("Linear Regression Training Accuracy: {}".format(accuracy_score(y_train, y_pred_train.round(), normalize=True, sample_weight=None)))

#Test accuracy on test set
y_pred_test=regr.predict(x_test)
print("Linear Regression Testing Accuracy: {}".format(accuracy_score(y_test, y_pred_test.round(), normalize=True, sample_weight=None)))


# ############################################### Random Forest Classifier ##############################################
# XXX
# TODO: Create a RandomForestClassifier and train it.
# XXX

#Create model
clf=RandomForestClassifier()

#Train model
clf.fit(x_train,y_train)

# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX

#Test accuracy on training set
y_pred_train=clf.predict(x_train)
print("Random Forest Training Accuracy: {}".format(accuracy_score(y_train, y_pred_train.round(), normalize=True, sample_weight=None)))

#Test accuracy on test set
y_pred_test=clf.predict(x_test)
print("Random Forest Testing Accuracy: {}".format(accuracy_score(y_test, y_pred_test.round(), normalize=True, sample_weight=None)))


# XXX
# TODO: Determine the feature importance as evaluated by the Random Forest Classifier.
#       Sort them in the descending order and print the feature numbers. The report the most important and the least important feature.
#       Mention the features with the exact names, e.g. X11, X1, etc.
#       Hint: There is a direct function available in sklearn to achieve this. Also checkout argsort() function in Python.
# XXX
feature_imp = pd.Series(clf.feature_importances_).sort_values(ascending=False)
print("Features sorted in decreasing order of importance")
for i in feature_imp.index:
    print("X{}".format(i),end=" ")
print()
print("Most important: X{}".format(feature_imp.idxmax()))
print("Least important: X{}".format(feature_imp.idxmin()))

# XXX
# TODO: Tune the hyper-parameters 'n_estimators' and 'max_depth'.
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX

#Specify parameters to be tuned
param_grid = {"n_estimators":[10,30,50,100],"max_depth":[9,11,15,20]}
grid_search = GridSearchCV(clf, param_grid=param_grid, cv=10, n_jobs=-1)
#start = time()

grid_search.fit(x_train, y_train)

print("Best parameters: {}".format(grid_search.best_params_))
print("Best score: {}".format(grid_search.best_score_))

new_clf=RandomForestClassifier(n_estimators=30,max_depth=20)
new_clf.fit(x_train,y_train)
y_pred_test=new_clf.predict(x_test)
print("Post-Tuning Random Forest Testing Accuracy: {}".format(accuracy_score(y_test, y_pred_test.round(), normalize=True, sample_weight=None)))



# ############################################ Support Vector Machine ###################################################
# XXX
# TODO: Pre-process the data to standardize or normalize it, otherwise the grid search will take much longer
# TODO: Create a SVC classifier and train it.
# XXX

scaler=StandardScaler().fit(x_train)

x_train_scaled=scaler.transform(x_train)
x_test_scaled=scaler.transform(x_test)

#Create classifier
svm=SVC(gamma='auto')

svm.fit(x_train,y_train)

# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX

#Test accuracy on training set
y_pred_train=svm.predict(x_train)
print("SVM Training Accuracy: {}".format(accuracy_score(y_train, y_pred_train.round(), normalize=True, sample_weight=None)))

#Test accuracy on test set
y_pred_test=svm.predict(x_test)
print("SVM Testing Accuracy: {}".format(accuracy_score(y_test, y_pred_test.round(), normalize=True, sample_weight=None)))


# XXX
# TODO: Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear).
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX
param_grid = {"C":[0.01,0.1,1.0,10],"kernel":["rbf","linear"]}
grid_search = GridSearchCV(svm, param_grid=param_grid, cv=10, n_jobs=-1)


grid_search.fit(x_train_scaled,y_train)

print("Best parameters: {}".format(grid_search.best_params_))
print("Best score: {}".format(grid_search.best_score_))

new_svm=SVC(C=10,kernel='rbf')
new_svm.fit(x_train_scaled,y_train)

y_pred_test=new_svm.predict(x_test_scaled)
print("Post-Tuning SVM Testing Accuracy: {}".format(accuracy_score(y_test, y_pred_test.round(), normalize=True, sample_weight=None)))

print("Mean fit time:",grid_search.cv_results_['mean_fit_time'][np.argmax(grid_search.cv_results_['mean_test_score'])])
print("Mean training score:",grid_search.cv_results_['mean_train_score'][np.argmax(grid_search.cv_results_['mean_test_score'])])


# ######################################### Principal Component Analysis #################################################
# XXX
# TODO: Perform dimensionality reduction of the data using PCA.
#       Set parameters n_component to 10 and svd_solver to 'full'. Keep other parameters at their default value.
#       Print the following arrays:
#       - Percentage of variance explained by each of the selected components
#       - The singular values corresponding to each of the selected components.
# XXX

pca=PCA(n_components=10,svd_solver='full')

pca.fit(x_data)
results=pca.transform(x_data)

print("PCA explained variance:",pca.explained_variance_ratio_   )
print("PC singular values:",pca.singular_values_)
