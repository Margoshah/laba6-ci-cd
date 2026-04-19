import pytest
from playwright.async_api import async_playwright
from .pages.ticket_page import TicketPage

@pytest.mark.asyncio
async def test_ticket_success():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        ticket = TicketPage(page)

        await ticket.open()
        await ticket.fill_form("AB123", "economy", 10) #проверкк рассчета для посажира с известым уровнем лояльности
        await ticket.submit()

        result = await ticket.get_result()
        assert result is not None
        assert "Итоговая цена" in result

        await browser.close()


@pytest.mark.parametrize("baggage, service_class, expected_price", [
    (10, "economy", "1800"),
    (25, "economy", "2250"), # доплата за перевес
    (10, "business", "2700"),# доплата за перевес
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

        result = await ticket.get_result()

        assert expected_price in result

        await browser.close()


@pytest.mark.parametrize("passport, s_class, baggage, expected_substring", [
    ("", "economy", 10, "заполните"),  # Проверка пустого паспорта
    ("AB123", "economy", -5, "отрицательным"),  # Отрицательный вес
    ("ABC", "economy", 10, "формат"),  # Несуществующий/неверный формат
    ("AB123", "", 10, "заполните"),
])
@pytest.mark.asyncio
async def test_ticket_negative_scenarios(passport, s_class, baggage, expected_substring):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        ticket = TicketPage(page)

        await ticket.open()

        if passport:
            await ticket.page.fill(ticket.passport, passport)

        await ticket.page.select_option(ticket.service_class, s_class)
        await ticket.page.fill(ticket.baggage, str(baggage))

        await ticket.submit()

        result = await ticket.get_result()
        assert expected_substring in result.lower()
        await browser.close()