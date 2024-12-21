def fibonacci_series(n):
    fib = [0, 1]
    while len(fib) < n:
        fib.append(fib[-1] + fib[-2])
    return fib[:n]

num = int(input("Enter the number of terms for the Fibonacci series: "))
print(f"Fibonacci series up to {num} terms: {fibonacci_series(num)}")
