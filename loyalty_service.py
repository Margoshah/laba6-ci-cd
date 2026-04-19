class LoyaltyService:

    async def get_discount(self, passport: str) -> float:
        # Простая заглушка для лабораторной

        if passport == "AB123":
            return 0.1   # 10% скидка

        return 0.0