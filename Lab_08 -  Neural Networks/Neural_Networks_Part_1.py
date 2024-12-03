# Part 1: Modified Neural Network on Iris Dataset


# Required Libraries
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

# Helper function to plot metrics
def plot_metrics(history, title="Model Metrics"):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    # Plot loss
    axes[0].plot(history.history['loss'], label='Train Loss')
    axes[0].plot(history.history['val_loss'], label='Validation Loss')
    axes[0].set_title(f'{title} - Loss')
    axes[0].set_xlabel('Epochs')
    axes[0].set_ylabel('Loss')
    axes[0].legend()
    
    # Plot accuracy
    axes[1].plot(history.history['accuracy'], label='Train Accuracy')
    axes[1].plot(history.history['val_accuracy'], label='Validation Accuracy')
    axes[1].set_title(f'{title} - Accuracy')
    axes[1].set_xlabel('Epochs')
    axes[1].set_ylabel('Accuracy')
    axes[1].legend()
    plt.tight_layout()
    plt.show()

# Load and preprocess Iris dataset
iris = load_iris()
X_iris = iris.data
y_iris = to_categorical(iris.target)

X_train, X_test, y_train, y_test = train_test_split(X_iris, y_iris, test_size=0.2, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size=0.5, random_state=42)

# Build the modified neural network
model_iris = Sequential([
    Dense(10, input_shape=(X_iris.shape[1],), activation='relu'),
    Dense(16, activation='relu'),  # Additional hidden layer
    Dense(3, activation='softmax')
])

model_iris.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history_iris = model_iris.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=50, batch_size=8, verbose=0)

# Evaluate the model
test_loss_iris, test_accuracy_iris = model_iris.evaluate(X_test, y_test, verbose=0)

# Plot metrics
plot_metrics(history_iris, title="Iris Dataset")
