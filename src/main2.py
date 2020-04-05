from data_builder import *

X = np.array([1,2,3,4,5,6,7,8,9])
y = [1,2,3,4,5,6,7,8,9]

X, y = create_window(X,y,window = 2)

print(X)
print(y)