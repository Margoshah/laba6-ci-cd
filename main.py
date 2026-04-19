from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ticketprice import calculate_ticket_price
from loyalty_service import LoyaltyService

app = FastAPI()

#модель запроса
class TicketRequest(BaseModel):
    base_price: float
    baggage_weight: float
    service_class: str
    passport: str


@app.post("/api/tickets/calculate")
async def calculate_ticket(data: TicketRequest):

    loyalty_service = LoyaltyService()

    try:
        price = await calculate_ticket_price(
            data.base_price,
            data.baggage_weight,
            data.service_class,
            data.passport,
            loyalty_service
        )

        return {
            "status": "success",
            "final_price": round(price, 2)
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/loyalty/{passport}")
async def get_loyalty(passport: str):

    loyalty_service = LoyaltyService()
    discount = await loyalty_service.get_discount(passport)

    return {
        "passport": passport,
        "discount": discount
    }


@app.get("/api/status")
async def status():
    return {"status": "online"}

from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="public", html=True), name="static")