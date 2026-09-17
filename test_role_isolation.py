import requests

print('=== Role Isolation Test ===')
print('Testing maint1 access to Administrator and Drone Operator endpoints...')

response = requests.post('http://localhost:8000/api/v1/auth/login', data={'username': 'maint1', 'password': 'Maint1Test123!'})
if response.status_code == 200:
    token = response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test Administrator-only endpoints
    print('\n--- Testing Administrator endpoints ---')
    
    # Try to access users list (Admin only)
    users_response = requests.get('http://localhost:8000/api/v1/users/', headers=headers)
    print(f'GET /users/ (Admin only): {users_response.status_code}')
    if users_response.status_code == 403:
        print('  ✅ Correctly denied')
    else:
        print(f'  ❌ Unexpected: {users_response.text}')
    
    # Try to create user (Admin only)
    create_user_response = requests.post('http://localhost:8000/api/v1/users/', 
                                        json={'username': 'test', 'email': 'test@test.com', 'password': 'Test123!', 'role': 'maintenance_engineer'}, 
                                        headers=headers)
    print(f'POST /users/ (Admin only): {create_user_response.status_code}')
    if create_user_response.status_code == 403:
        print('  ✅ Correctly denied')
    else:
        print(f'  ❌ Unexpected: {create_user_response.text}')
    
    # Test that maint1 CAN access Maintenance Engineer endpoints
    print('\n--- Testing Maintenance Engineer endpoints ---')
    
    # Telemetry predict (Maintenance Engineer only)
    predict_response = requests.post('http://localhost:8000/api/v1/telemetry/predict', 
                                     json={'current': 15.0, 'temperature': 45.0}, 
                                     headers=headers)
    print(f'POST /telemetry/predict (Maintenance Engineer): {predict_response.status_code}')
    if predict_response.status_code == 200:
        print('  ✅ Correctly allowed')
    else:
        print(f'  ❌ Unexpected: {predict_response.text}')
    
    # Telemetry simulate (Maintenance Engineer only)
    sim_response = requests.post('http://localhost:8000/api/v1/telemetry/simulate', 
                                 json={'samples': 5, 'scenario': 'healthy', 'seed': 42}, 
                                 headers=headers)
    print(f'POST /telemetry/simulate (Maintenance Engineer): {sim_response.status_code}')
    if sim_response.status_code == 201:
        print('  ✅ Correctly allowed')
    else:
        print(f'  ❌ Unexpected: {sim_response.text}')
    
else:
    print(f'Login failed: {response.status_code}')
