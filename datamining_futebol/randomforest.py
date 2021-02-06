import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

print('lendo dados')
features = pd.read_csv('eventos_final.csv')
features.head(5)
temp=features.describe()

print('separando dados')
labels=np.array(features['Impedimento'])
features=features.drop('Impedimento',axis=1)
feature_list=list(features.columns)
features=np.array(features)
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)

roc_auc=[]
accuracy=[]
errors=[]
confusao=[]
for i in range(5):
    print(i)
    print('classificando dados')
    rfc=RandomForestClassifier(n_estimators=10**i,random_state=0)
    rfc.fit(train_features,train_labels)
    pred_labels=rfc.predict(test_features)
    
    print('medindo resultados')
    from sklearn.metrics import roc_curve, auc
    false_positive_rate, true_positive_rate, thresholds = roc_curve(test_labels, pred_labels)
    roc_auc.append(auc(false_positive_rate, true_positive_rate))
    
    accuracy.append(metrics.accuracy_score(test_labels,pred_labels))
    errors.append(abs(pred_labels - test_labels)/len(test_labels))
    confusao.append(metrics.confusion_matrix(test_labels,pred_labels))
#
#
#print('apresentando uma DT')
## Import tools needed for visualization
#from sklearn.tree import export_graphviz
#import pydot
## Pull out one tree from the forest
#tree = rfc.estimators_[5]
## Export the image to a dot file
#export_graphviz(tree, out_file = 'tree.dot', feature_names = feature_list, rounded = True, precision = 1)
## Use dot file to create a graph
#(graph, ) = pydot.graph_from_dot_file('tree.dot')
## Write graph to a png file
#graph.write_png('tree.png')