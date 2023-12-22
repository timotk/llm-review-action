def calculate_average(numbers):
    # Initialize the sum and count variables
    sum = 0
    count = 0

    # Iterate over the numbers list
    for num in numbers:
        sum += num
        count += 1

    # Calculate the average
    average = sum / count

    # Return the average
    return average
