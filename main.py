import csv
from math import sqrt
from tkinter import Tk, Label, Entry, Button

import matplotlib.pyplot as plt


# Funkcja wczytująca dane z pliku CSV
def load_csv(filename):
    dataset = []
    with open(filename, 'r') as file:
        csvReader = csv.reader(file, delimiter=';')
        for row in csvReader:
            if not row:
                continue
            dataset.append(row)
    return dataset


# Funkcja zamieniająca wartości tekstowe kolumn na wartości liczbowe
def str_to_float(dataset, column):
    values = [row[column] for row in dataset]
    try:
        float(values[0])
        for i in range(len(dataset)):
            dataset[i][column] = float(dataset[i][column])
    except ValueError:
        pass


# Funkcja obliczająca odległość euklidesową między dwoma wektorami
def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1) - 1):
        distance += (row1[i] - row2[i]) ** 2
    return sqrt(distance)


# Funkcja zwracająca k najbliższych sąsiadów
def get_neighbors(train, test_row, k):
    distances = []
    for train_row in train:
        distance = euclidean_distance(test_row, train_row)
        distances.append((train_row, distance))
    distances.sort(key=lambda x: x[1])
    neighbors = []
    for i in range(k):
        neighbors.append(distances[i][0])
    return neighbors


# Funkcja dokonująca klasyfikacj i
def predict_classification(train, test_row, k):
    neighbors = get_neighbors(train, test_row, k)
    output_values = [row[-1] for row in neighbors]
    prediction = max(set(output_values), key=output_values.count)
    return prediction


# Funkcja obliczająca dokładność klasyfikacji
def accuracy_of_classification(actual, predicted):
    correct = 0
    for i in range(len(actual)):
        if actual[i] == predicted[i]:
            correct += 1
    return correct / float(len(actual)) * 100.0


# Funkcja wykonująca klasyfikację dla całego zbioru testowego
def k_nearest_neighbors(train, test, k):
    predictions = []
    for test_row in test:
        output = predict_classification(train, test_row, k)
        predictions.append(output)
    return predictions


# Funkcja obsługująca przycisk i wykonująca klasyfikację
def classify():
    k = int(k_entry.get())
    train_filename = train_entry.get()
    test_filename = test_entry.get()
    train_set = load_csv(train_filename)
    test_set = load_csv(test_filename)
    for i in range(len(train_set[0]) - 1):
        str_to_float(train_set, i)
        str_to_float(test_set, i)
    k_values = range(1, k)
    accuracies = []
    for k in k_values:
        predicted = k_nearest_neighbors(train_set, test_set, k)
        actual = [row[-1] for row in test_set]
        accuracy = accuracy_of_classification(actual, predicted)
        accuracies.append(accuracy)
        print('k=%d, accuracy=%.2f%%' % (k, accuracy))
    plt.plot(k_values, accuracies, color='purple')
    plt.xlabel('k')
    plt.ylabel('accuracy (%)')
    plt.title('Accuracy Chart')
    plt.show()


# Tworzenie okna Tkinter
window = Tk()

# Tworzenie etykiet i pól wprowadzania danych
k_label = Label(window, text="Enter k argument:")
k_entry = Entry(window)
train_label = Label(window, text="Enter train set file name:")
train_entry = Entry(window)
test_label = Label(window, text="Enter test set file name:")
test_entry = Entry(window)

# Tworzenie przycisku
classify_button = Button(window, text="Classify", command=classify)

# Pozycjonowanie elementów w oknie
k_label.grid(row=0, column=0)
k_entry.grid(row=0, column=1)
train_label.grid(row=1, column=0)
train_entry.grid(row=1, column=1)
test_label.grid(row=2, column=0)
test_entry.grid(row=2, column=1)
classify_button.grid(row=3, columnspan=2)

# Uruchomienie pętli obsługi zdarzeń
window.mainloop()
