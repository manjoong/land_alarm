#-*-coding:utf-8 -*-


from pyfcm import FCMNotification

push_service = FCMNotification(api_key="AAAADgTMcII:APA91bFMVVBZB7bOM8BqocEGTJToANS9sB4Da0ODqG4RTfndoUapWBye8ASi9d3-rHUCkq4BvabFLgSqBfdyqrxtWCqZj3lYSYXpsFB-Szvo4gEgh9cExF24Puvr3I9rQ7r-H-pWMMQ0")

push_tokens = ["cNTL3jvGjWA:APA91bFYdH88xieN8RRCekqH8WMM8j9KFz1NpHlzXSE8s3ooMutiSgnAoZHaVD48iGh1EW6o_fX1Sur17-nVkCnSatYvG43DD9pITNlmB9phhe1gMPl_1rou4NY2BetKarN3FNEMWDo1"]
message_title = "manjoong!!"
message_body = "gotcha!!!"
result = push_service.notify_multiple_devices(registration_ids=push_tokens, message_title=message_title, message_body=message_body)
		

# result = push_service.notify_single_device(registration_id=push_tokens, message_title=message_title, message_body=message_body)

# cNTL3jvGjWA:APA91bFYdH88xieN8RRCekqH8WMM8j9KFz1NpHlzXSE8s3ooMutiSgnAoZHaVD48iGh1EW6o_fX1Sur17-nVkCnSatYvG43DD9pITNlmB9phhe1gMPl_1rou4NY2BetKarN3FNEMWDo1