import matplotlib.pyplot as plt

# Data points for the first encoding method
nodes1 = [2, 4, 6]
time1 = [3.2567808628082275, 19.710580110549927, 1141.203]

# Data points for the second encoding method
nodes2 = [2, 4, 6]
time2 = [0.6269831657409668, 1.8318147659301758, 300]

# Plotting the graphs
plt.figure(figsize=(10, 5))

# First encoding method
plt.plot(nodes1, time1, label='First Encoding Method', marker='o')

# Second encoding method
plt.plot(nodes2, time2, label='Second Encoding Method', marker='o')

# Adding titles and labels
plt.title('Performance Comparison of Two Encoding Methods')
plt.xlabel('Number of Nodes')
plt.ylabel('Time (seconds)')
plt.yscale('log')  # Log scale for better visualization of large values

# Adding a legend
plt.legend()

# Displaying the plot
plt.show()
