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

        # Ждем появления элемента и текста "Итоговая цена"
        result_locator = page.locator("#result-price")
        await result_locator.wait_for(state="visible")

        # Небольшая пауза, чтобы JS успел обновить текст
        await asyncio.sleep(1)

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

        result_locator = page.locator("#result-price")
        await result_locator.wait_for(state="visible")
        await asyncio.sleep(1)

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
        if s_class:
            await ticket.page.select_option(ticket.service_class, s_class)
        await ticket.page.fill(ticket.baggage, str(baggage))
        await ticket.submit()

        result_locator = page.locator("#result-price")
        await result_locator.wait_for(state="visible")
        await asyncio.sleep(1)

        result = await ticket.get_result()
        assert expected_substring in result.lower()
        await browser.close()