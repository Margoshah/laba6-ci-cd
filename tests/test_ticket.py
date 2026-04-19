import pytest
from playwright.async_api import async_playwright
from .pages.ticket_page import TicketPage


@pytest.mark.asyncio
async def test_ticket_success():
    async with async_playwright() as p:
        # ОБЯЗАТЕЛЬНО headless=True для GitHub
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        ticket = TicketPage(page)

        await ticket.open()
        await ticket.fill_form("AB123", "economy", 10)
        await ticket.submit()

        # Ждем, пока текст внутри элемента изменится с заглушки на результат
        await page.wait_for_function(
            'document.querySelector("#result-price").innerText.includes("Итоговая цена")'
        )

        result = await ticket.get_result()
        assert result is not None
        assert "Итоговая цена" in result
        await browser.close()


@pytest.mark.parametrize("baggage, service_class, expected_price", [
    (10, "economy", "1800"),
    (25, "economy", "2250"),
    (10, "business", "2700"),
])
@pytest.mark.asyncio
async def test_ticket_variants(baggage, service_class, expected_price):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        ticket = TicketPage(page)

        await ticket.open()
        await ticket.fill_form("AB123", service_class, baggage)
        await ticket.submit()

        # Ждем появления конкретной ожидаемой цены
        await page.wait_for_selector(f"text={expected_price}")

        result = await ticket.get_result()
        assert expected_price in result
        await browser.close()


@pytest.mark.parametrize("passport, s_class, baggage, expected_substring", [
    ("", "economy", 10, "заполните"),
    ("AB123", "economy", -5, "отрицательным"),
    ("ABC", "economy", 10, "формат"),
])
@pytest.mark.asyncio
async def test_ticket_negative_scenarios(passport, s_class, baggage, expected_substring):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        ticket = TicketPage(page)

        await ticket.open()
        if passport:
            await ticket.page.fill(ticket.passport, passport)

        # Обработка выбора класса, если он не пустой
        if s_class:
            await ticket.page.select_option(ticket.service_class, s_class)

        await ticket.page.fill(ticket.baggage, str(baggage))
        await ticket.submit()

        # Ждем появления текста ошибки
        await page.wait_for_function(
            f'document.querySelector("#result-price").innerText.toLowerCase().includes("{expected_substring}")'
        )

        result = await ticket.get_result()
        assert expected_substring in result.lower()
        await browser.close()