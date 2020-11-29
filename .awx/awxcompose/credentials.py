DATABASES = {
    'default': {
        'ATOMIC_REQUESTS': True,
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "awx",
        'USER': "awx",
        'PASSWORD': "awxpass",
        'HOST': "postgres",
        'PORT': "5432",
    }
}

BROADCAST_WEBSOCKET_SECRET = "M3dJLmoxR0s4RDJGY3BfNDhxRGtOallEUk42bk5qWGxjVFloR2tESW9rNXNhaXdjVmRMNnV2WUV6LDdGazpCeDNteklFUUs6dTBTT2U1QTRtd1dzT0ZpY0JBZUdzai4sWXMyTkVwZXByMWdiQ0JmSFlnNUg1ZXBJdVlMSm1URWg="
