import re
async def calculate_ticket_price(
    base_price: float,
    baggage_weight: float,
    service_class: str,
    passport: str,
    loyalty_service
):
    if not re.match(r"^[A-Z]{2}\d{3}$", passport):
        raise ValueError("Некорректный формат паспорта. Используйте формат AA111")

    if base_price < 1000:
        raise ValueError("Цена ниже минимального значения")

    if baggage_weight < 0:
        raise ValueError("Вес багажа не может быть отрицательным")

    if service_class not in ("economy", "business"):
        raise ValueError("Некорректный класс обслуживания")

    price = base_price

    if baggage_weight > 20:
        price += 500

    if service_class == "business":
        price *= 1.5

    # Асинхронный вызов внешнего сервиса
    try:
        discount = await loyalty_service.get_discount(passport)
    except Exception:
        discount = 0.0

    price *= (1 - discount)

    return price
