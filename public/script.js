async function send() {
    const passport = document.getElementById("passport").value;
    const service_class = document.getElementById("class").value;
    const baggageValue = document.getElementById("baggage").value;
    const resultDiv = document.getElementById("result");

    //валидация перед отправкой
    if (!passport || !service_class || !baggageValue) {
        resultDiv.innerText = "Заполните все поля!";
        resultDiv.style.color = "red";
        return;
    }

    try {
        const res = await fetch("/api/tickets/calculate", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                passport: passport,
                service_class: service_class,
                baggage_weight: parseFloat(baggageValue),
                base_price: 2000 // Базовая цена по умолчанию
            })
        });

        const data = await res.json();

        if (res.ok) {
            resultDiv.innerText = `Итоговая цена: ${data.final_price} руб.`;
            resultDiv.style.color = "#2d5afc";
        } else {
            resultDiv.innerText = `Ошибка: ${data.detail}`;
            resultDiv.style.color = "red";
        }
    } catch (error) {
        resultDiv.innerText = "Ошибка соединения с сервером";
    }
}
function clearForm() {
    document.getElementById("passport").value = "";
    document.getElementById("class").value = "";
    document.getElementById("baggage").value = "";
    const resultDiv = document.getElementById("result");
    resultDiv.innerText = "Здесь будет стоимость...";
    resultDiv.style.color = "#2d5afc";
}