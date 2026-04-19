import pytest
from unittest.mock import AsyncMock
from ticketprice import calculate_ticket_price


# позитивные СЦЕНАРИИ

@pytest.mark.asyncio
async def test_economy_without_baggage_fee():
    loyalty_mock = AsyncMock()
    loyalty_mock.get_discount.return_value = 0

    result = await calculate_ticket_price(
        2000, 10, "economy", "AB123", loyalty_mock
    )

    assert result == 2000


@pytest.mark.asyncio
async def test_economy_with_baggage_fee():
    loyalty_mock = AsyncMock()
    loyalty_mock.get_discount.return_value = 0

    result = await calculate_ticket_price(
        2000, 25, "economy", "AB123", loyalty_mock
    )

    assert result == 2500


@pytest.mark.asyncio
async def test_business_class_with_overweight():
    loyalty_mock = AsyncMock()
    loyalty_mock.get_discount.return_value = 0

    result = await calculate_ticket_price(
        2000, 30, "business", "AB123", loyalty_mock
    )

    assert result == (2000 + 500) * 1.5

# НОВАЯ ЛОГИКА — СКИДКИ

@pytest.mark.asyncio
async def test_discount_applied_economy():
    loyalty_mock = AsyncMock() #фейковый сервис скидок.
    loyalty_mock.get_discount.return_value = 0.1

    result = await calculate_ticket_price(
        2000, 10, "economy", "AB123", loyalty_mock
    )

    assert result == 1800
    loyalty_mock.get_discount.assert_awaited_once_with("AB123")#был ли вызван,сколько раз с каким аргументом


@pytest.mark.asyncio
async def test_discount_applied_business_with_overweight():
    loyalty_mock = AsyncMock()
    loyalty_mock.get_discount.return_value = 0.2

    result = await calculate_ticket_price(
        2000, 30, "business", "AB123", loyalty_mock
    )
    assert result == 3000


@pytest.mark.asyncio
async def test_loyalty_service_failure():
    loyalty_mock = AsyncMock()
    loyalty_mock.get_discount.side_effect = Exception("Service error")

    result = await calculate_ticket_price(
        2000, 30, "economy", "AB123", loyalty_mock
    )

    assert result == 2500


@pytest.mark.asyncio
async def test_discount_zero():
    loyalty_mock = AsyncMock()
    loyalty_mock.get_discount.return_value = 0

    result = await calculate_ticket_price(
        2000, 10, "economy", "AB123", loyalty_mock
    )

    assert result == 2000


# НЕГАТИВНЫЕ СЦЕНАРИИ

@pytest.mark.asyncio
async def test_base_price_too_low():
    loyalty_mock = AsyncMock()

    with pytest.raises(ValueError):
        await calculate_ticket_price(
            500, 10, "economy", "AB123", loyalty_mock
        )


@pytest.mark.asyncio
async def test_negative_baggage_weight():
    loyalty_mock = AsyncMock()

    with pytest.raises(ValueError):
        await calculate_ticket_price(
            2000, -5, "economy", "AB123", loyalty_mock
        )


@pytest.mark.asyncio
async def test_invalid_service_class():
    loyalty_mock = AsyncMock()

    with pytest.raises(ValueError):
        await calculate_ticket_price(
            2000, 10, "vip", "AB123", loyalty_mock
        )


# ГРАНИЧНЫЕ ЗНАЧЕНИЯ

@pytest.mark.asyncio
async def test_zero_baggage_weight():
    loyalty_mock = AsyncMock()
    loyalty_mock.get_discount.return_value = 0

    result = await calculate_ticket_price(
        2000, 0, "economy", "AB123", loyalty_mock
    )

    assert result == 2000


@pytest.mark.asyncio
async def test_baggage_exactly_limit():
    loyalty_mock = AsyncMock()
    loyalty_mock.get_discount.return_value = 0

    result = await calculate_ticket_price(
        2000, 20, "economy", "AB123", loyalty_mock
    )

    assert result == 2000


@pytest.mark.asyncio
async def test_base_price_min_limit():
    loyalty_mock = AsyncMock()
    loyalty_mock.get_discount.return_value = 0

    result = await calculate_ticket_price(
        1000, 10, "economy", "AB123", loyalty_mock
    )

    assert result == 1000
