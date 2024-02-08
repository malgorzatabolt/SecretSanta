import smtplib
MY_EMAIL = "malgorzatabolt00@gmail.com"
PASSWORD = "aogxyvpqxrkrkcwt"


class Postman:
    def __init__(self, email, msg):
        self.email = email
        self.msg = msg

    def send_msg(self):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=self.email,
                msg=self.msg)
