import pytest
import asyncio
from playwright.async_api import async_playwright
from .pages.ticket_page import TicketPage


@pytest.mark.asyncio
async def test_ticket_success():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        ticket = TicketPage(page)

        await ticket.open()
        await ticket.fill_form("AB123", "economy", 10)
        await ticket.submit()

        # ИСПРАВЛЕНИЕ: Ждем, пока в блоке результата появится слово "Итоговая"
        # Это гарантирует, что расчет завершен
        await page.wait_for_selector(f"{ticket.result}:has-text('Итоговая')", timeout=10000)

        result = await ticket.get_result()
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

        # ИСПРАВЛЕНИЕ: Ждем, пока появится конкретная цена, которую мы ожидаем
        await page.wait_for_selector(f"{ticket.result}:has-text('{expected_price}')", timeout=10000)

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
        # Заполняем поля вручную через страницу, чтобы обойти fill_form если нужно
        if passport:
            await page.fill(ticket.passport, passport)
        await page.select_option(ticket.service_class, s_class)
        await page.fill(ticket.baggage, str(baggage))

        await ticket.submit()

        # Ждем появления текста ошибки в блоке результата
        await page.wait_for_selector(f"{ticket.result}:has-text('{expected_substring}')", timeout=10000)

        result = await ticket.get_result()
        assert expected_substring in result.lower()
        await browser.close()