Feature: Расчет стоимости авиабилета

Scenario Outline: расчет цены билета

Given сервис доступен
And паспорт "<passport>"
And базовая цена <base_price>
And вес багажа <baggage_weight>
And класс "<service_class>"

When я отправляю запрос на расчет

Then API возвращает статус 200

Examples:
| passport | base_price | baggage_weight | service_class |
| AB123 | 2000 | 10 | economy |
| AB123 | 2000 | 25 | economy |
| AB123 | 2000 | 10 | business |
| AB123 | 2000 | 30 | business |