# Update interval to store the latest position received
POSTGRES_WINDOW = int(2*60)  # in seconds

# Update interval to fetch messages from aishub api
AISHUBAPI_WINDOW = 1*60  # in seconds

# If set to False, shipinfos history won't be saved
KEEP_SHIPINFOS_HISTORY = False
