import smtplib
my_email = "malgorzatabolt00@gmail.com"
password = "aogxyvpqxrkrkcwt"


class Postman:
    def __init__(self, email, msg):
        self.email = email
        self.msg = msg

    def send_msg(self):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=self.email,
                msg=self.msg)
