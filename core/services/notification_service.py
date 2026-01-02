from django.core.mail import EmailMultiAlternatives


def notify_manager(ad):
    subject = "Оголошення потребує модерації"
    text_content = f"""
    Оголошення з ID: {ad.id} не пройшло модерацію та було відмічено як неактивне.

    Деталі оголошення:
    Бренд: {ad.brand}
    Модель: {ad.model}
    Місто: {ad.city}
    Користувач: {ad.user.email}

    Просимо вас перевірити оголошення та вжити відповідних заходів.

    З повагою,
    Команда AutoRIA
    """

    html_content = f"""
    <h2>Оголошення потребує модерації</h2>
    <p><b>ID:</b> {ad.id}</p>
    <p><b>Бренд:</b> {ad.brand}</p>
    <p><b>Модель:</b> {ad.model}</p>
    <p><b>Місто:</b> {ad.city}</p>
    <p><b>Користувач:</b> {ad.user.email}</p>
    <p>Просимо вас перевірити оголошення та вжити відповідних заходів.</p>
    <br>
    <p>З повагою,<br>Команда AutoRIA</p>
    """

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        None,
        ["yourEmailHere@gmail.com"],  # teacher can change recipient
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
