from flask_mail import Message
from extensions import mail


def send_purchase_email(email, product):

    msg = Message(
        "Purchase Confirmation",
        sender="myshop@gmail.com",
        recipients=[email]
    )

    msg.body = f"""

Hello,

Thank you for purchasing:

{product.name}

Amount:
Ksh {product.price}

Your order has been received successfully.

Thank you for shopping with TruHome.

"""

    mail.send(msg)