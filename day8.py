#warmup.py
print("warmup start")
nums = [1,2,3]
nums.append(4)
print(nums)
nums.remove(2)
print(nums)
print("warmup end")

# list_crud.py
users = []
users.append("lewis")
users.append("mark")
print("After add:", users)

print("First user:", users[0])

users[1] = "brian"
print("After update:", users)

users.remove("lewis")
print("After delete:", users)

# dict_crud.py
student = {"id": 1, "name": "lewis", "age": 21}
print("Name:", student["Name"])