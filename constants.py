BASE_API_URL = 'https://api.postmates.com'

API_KEY = '5ca53576-4212-4c2d-8108-14933d31996b'
CUSTOMER_ID = 'cus_Mpj4UY4RWY7m9-'

QUOTE_ENDPOINT = BASE_API_URL + '/v1/customers/%s/delivery_quotes' % (CUSTOMER_ID)
DELIVERY_ENDPOINT = BASE_API_URL + '/v1/customers/%s/deliveries' % (CUSTOMER_ID)
