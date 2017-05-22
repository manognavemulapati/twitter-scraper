from twilio.rest import Client

class SMS :
    account_sid = "AC7d21997a0c0915bb123f3236d4dc1473"
    auth_token = "745720eef07c275e447c856193432539"

    client = Client(account_sid, auth_token)

    def __init__ (self, message, to_num, from_num) :
        self.message = message
        self.to_num = to_num
        self.from_num = from_num

    def send_sms (self) :
        self.client.messages.create(
                       to=self.to_num,
                       from_=self.from_num,
                       body=self.message
                       )
