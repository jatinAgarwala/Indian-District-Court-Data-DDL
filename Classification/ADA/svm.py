import numpy as np
from sklearn import svm

from data import train, test, valid

# Convert the training and test sets to NumPy arrays
X_train = np.array(train[0])
y_train = np.array(train[1])
X_test = np.array(valid[0])
y_test = np.array(valid[1])

# Create an SVM classifier
clf = svm.SVC(kernel='linear')

# Train the classifier on the training set
clf.fit(X_train, y_train)

# Test the classifier on the test set
accuracy = clf.score(X_test, y_test)

print('Test accuracy: {:.2f}%'.format(accuracy * 100))

# Make predictions on new data
predictions = clf.predict(test[0])
