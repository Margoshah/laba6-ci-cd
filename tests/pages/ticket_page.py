class TicketPage:
    def __init__(self, page):#способы поиска элементов на странице
        self.page = page
        self.passport = "#passport"
        self.service_class = "#class"
        self.baggage = "#baggage"
        self.button = "text=Рассчитать"
        self.result = "#result"

    async def open(self):
        await self.page.goto("http://127.0.0.1:8000")

    async def fill_form(self, passport, service_class, baggage):
        await self.page.fill(self.passport, passport)
        await self.page.select_option(self.service_class, service_class)
        await self.page.fill(self.baggage, str(baggage))

    async def submit(self):
        await self.page.click(self.button)

    async def get_result(self):
        return await self.page.text_content(self.result)