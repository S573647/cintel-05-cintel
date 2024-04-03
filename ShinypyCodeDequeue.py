from collections import deque

# Create an empty deque
empty_deque = deque()
print(empty_deque) 

# Create a deque by passing in a list with values
temp_deque_F = deque( [56, 58, 47, 54, 55] )
print(temp_deque_F)  

# Create a deque by passing in a list variable
temp_list_C = [5, 6, 8, 4, 3, 2]
temp_deque_C = deque( temp_list_C )
print(temp_deque_C )
temp_deque_F.append(60)
temp_deque_F.append(62)
temp_deque_F.append(64)
temp_deque_F.append(61)
print("After inserting elements ")
print(temp_deque_F)  

temp_deque_F.pop()  
print("After deleting elements at the end ")
print(temp_deque_F) 
temp_deque_F.popleft() 
print("After deleting left element ")
print(temp_deque_F) 

length=len(temp_deque_F)  
print("length of the dequeue : " ,length)

temp_deque_F.clear() 
length=len(temp_deque_F)  
print("length of the dequeue after clear : " ,length)

# Initialize deque with a max length of 3 to store last 3 stock prices
msft_prices = deque(maxlen=3)

# Clear the deque (we might call this at the start of a new day)
msft_prices.clear()

# Simulate updating the stock price with new values
msft_prices.append(310.35)
print("MSFT stock prices:", list(msft_prices))

msft_prices.append(312.31)
print("MSFT stock prices:", list(msft_prices))

msft_prices.append(315.25)
print("MSFT stock prices:", list(msft_prices))

msft_prices.append(317.41)
print("MSFT stock prices:", list(msft_prices))
