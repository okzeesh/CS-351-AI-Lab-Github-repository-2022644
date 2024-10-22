# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Step 1: Create a simple dataset
# Manpower (independent variable) and corresponding Work Done (dependent variable)
manpower = np.array([20, 10, 15, 40, 50, 60, 80, 100, 120, 150, 200]).reshape(-1, 1)
work_done = np.array([50, 25, 37, 100, 120, 150, 200, 250, 300, 370, 500])

# Step 2: Visualize the data
plt.scatter(manpower, work_done, color='blue')
plt.title('Manpower vs. Work Done')
plt.xlabel('Manpower')
plt.ylabel('Work Done')
plt.show()

# Step 3: Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(manpower, work_done, test_size=0.2, random_state=42)

# Step 4: Create and train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 5: Visualize the fitted line on the training data
plt.scatter(X_train, y_train, color='blue', label='Training Data')
plt.plot(X_train, model.predict(X_train), color='red', label='Fitted Line')
plt.title('Linear Regression Fit on Training Data')
plt.xlabel('Manpower')
plt.ylabel('Work Done')
plt.legend()
plt.show()

# Step 6: Visualize the fitted line on both training and test data
plt.scatter(X_train, y_train, color='blue', label='Training Data')
plt.scatter(X_test, y_test, color='green', label='Test Data')
plt.plot(manpower, model.predict(manpower), color='red', label='Fitted Line')
plt.title('Linear Regression Fit on Training and Test Data')
plt.xlabel('Manpower')
plt.ylabel('Work Done')
plt.legend()
plt.show()

# Step 7: Make predictions on the test set and visualize
y_pred = model.predict(X_test)
plt.scatter(X_test, y_test, color='green', label='Actual Test Data')
plt.scatter(X_test, y_pred, color='red', marker='x', label='Predicted Test Data')
plt.title('Test Data Predictions')
plt.xlabel('Manpower')
plt.ylabel('Work Done')
plt.legend()
plt.show()

# Step 8: Display the model's slope (coefficient) and intercept
slope = model.coef_[0]
intercept = model.intercept_
print(f'Slope (Coefficient): {slope}')
print(f'Intercept: {intercept}')

# Step 9: Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error (MSE): {mse}')
print(f'R-squared: {r2}')
