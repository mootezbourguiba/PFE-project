from services.api import login

response = login(
    "admin",
    "admin123"
)

print(response.status_code)
print(response.json())