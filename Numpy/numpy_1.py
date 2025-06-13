# 1D Array Operations with NumPy

import numpy as np

# Create a 1D array
arr = np.array([1, 2, 3, 4, 5])
print("1D Array:", arr)

# Ones and Zeros

arr0 = np.zeros(5)  # Create an array of zeros
arr1 = np.ones(5)   # Create an array of ones
print("Array of Zeros:", arr0)
print("Array of Ones:", arr1)

# add 10 to each element
arr += 10
print("Modified 1D Array:", arr)

# add a number at the end
arr = np.append(arr, 6)
print("Appended 1D Array:", arr)

# add a number at the beginning
arr = np.insert(arr, 0, 0)
print("Inserted at Beginning:", arr)

# add a number at any position
arr = np.insert(arr, 3, 3.5)
print("Inserted at Position 3:", arr)

# sort the array using numpy
arr = np.sort(arr)
print("Sorted Array:", arr)

# reverse the array using numpy
arr = np.flip(arr)
print("Reversed Array:", arr)

# Search for an element in the array
index = np.where(arr == 3.5)
print("Index of 3.5:", index[0][0] if index[0].size > 0 else "Not found")

# Find the maximum and minimum values in the array
max_value = np.max(arr)
min_value = np.min(arr)
print("Maximum Value:", max_value)
print("Minimum Value:", min_value)

# Calculate the sum and mean of the array
# mean value = average of all elements
sum_value = np.sum(arr)
mean_value = np.mean(arr)
print("Sum of Array:", sum_value)
print("Mean of Array:", mean_value)

##### Calculate the standard deviation of the array #####
# standard deviation = measure of the amount of variation or dispersion of a set of values
# first, need to find mean
# Then, subtract the mean from each element
# Square the result, find the mean of those squared differences
# Finally, take the square root of that mean
# Absolute Cinema

std_dev = np.std(arr)
print("Standard Deviation of Array:", std_dev)

####### Calculate the variance of the array ######
# variance = measure of how far a set of numbers are spread out from their average value
# first, find the mean
# Then, subtract the mean from each element
# Square the result, find the mean of those squared differences
# Finally, that mean is the variance
variance = np.var(arr)
print("Variance of Array:", variance)

#### std_dev^2 is equal to variance

if std_dev**2 == variance:
    print("Standard Deviation squared is equal to Variance")
else:
    print("Standard Deviation squared is NOT equal to Variance")
    
# Find the unique elements in the array
unique_elements = np.unique(arr)
print("Unique Elements in Array:", unique_elements)

# Find the median of the array
# Absolute Moddhok
median_value = np.median(arr)
print("Median of Array:", median_value)

# Find the rms (root mean square) of the array
# rms = square root of the mean of the squares of the elements
rms_value = np.sqrt(np.mean(arr**2))
print("RMS of Array:", rms_value)

# Find the cumulative sum of the array
# kromojozito gonosongkha ahh
cumsum_value = np.cumsum(arr)
print("Cumulative Sum of Array:", cumsum_value)

# Find the cumulative product of the array

cumsum_product = np.cumprod(arr)
print("Cumulative Product of Array:", cumsum_product)

# Find the difference between consecutive elements
arr = np.array([1, 3, 6, 10, 15])
print("Original Array for Difference:", arr)
diff_value = np.diff(arr)
print("Difference between Consecutive Elements:", diff_value)

# displaying array without brackets
print("Array without brackets:", ' '.join(map(str, arr)))


