from behave import given, when, then
from fastapi.testclient import TestClient#ИНСТР ДЛЯ ТЕСТИРОВАНИЯ БЕЗ ЗАПСКА КОДА
from main import app

client = TestClient(app)

@given("сервис доступен")
def step_impl(context):
    response = client.get("/api/status")
    assert response.status_code == 200


@given('паспорт "{passport}"')
def step_impl(context, passport):
    context.passport = passport


@given('базовая цена {price}')
def step_impl(context, price):
    context.base_price = float(price)


@given('вес багажа {weight}')
def step_impl(context, weight):
    context.baggage_weight = float(weight)


@given('класс "{service_class}"')
def step_impl(context, service_class):
    context.service_class = service_class


@when("я отправляю запрос на расчет")
def step_impl(context):

    payload = {
        "base_price": context.base_price,
        "baggage_weight": context.baggage_weight,
        "service_class": context.service_class,
        "passport": context.passport
    }

    context.response = client.post(
        "/api/tickets/calculate",
        json=payload
    )


@then("API возвращает статус 200")
def step_impl(context):
    assert context.response.status_code == 200