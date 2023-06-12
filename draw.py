import matplotlib.pyplot as plt
def draw_figure(x_data, y_data, x, y_fit):
    # Plot the original data points and the fitted curve
    plt.scatter(x_data, y_data, color='red', label='Data Points')
    #plt.scatter(MAFV,MAF, color='purple', label='Original')
    plt.plot(x, y_fit, 'b-', label='Fitted Curve')

    # Set the labels and title
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Curve Fitting with Fitted Curve')

    # Display the legend
    plt.legend()

    # Show the plot
    plt.show()