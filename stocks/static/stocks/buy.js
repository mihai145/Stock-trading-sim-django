document.addEventListener('DOMContentLoaded', function () {
    document.querySelector("#buy-button").addEventListener('click', () => {
        ///clearing any previous feedback
        const prevFeedback = document.querySelector('.feedback');
        if (prevFeedback) {
            prevFeedback.remove();
        }

        const buyCard = document.querySelector("#buy-card");

        const amountField = document.querySelector("#bought-stocks");
        const val = amountField.value;
        amountField.value = '';

        if (amountField <= 0) {
            const feedback = document.createElement('p');
            feedback.classList.add("feedback");
            feedback.classList.add("my-2");
            feedback.innerHTML = `You cannout buy less than one share!`;
            buyCard.append(feedback);
        } else {
            const ticker = document.querySelector("#ticker").innerHTML;
            const pricePerShare = document.querySelector("#adjusted-buy").innerHTML;

            fetch(`/buy/${ticker}`, {
                    method: 'POST',
                    body: JSON.stringify({
                        amount: val,
                        pricePerShare: pricePerShare
                    })
                })
                .then(response => response.json())
                .then(result => {
                    if (result.message == "OK") {
                        const owned = document.querySelector("#owned-amount");
                        const newOwned = parseInt(owned.innerHTML) + parseInt(val);
                        owned.innerHTML = newOwned.toString();

                        const feedback = document.createElement('p');
                        feedback.classList.add("feedback");
                        feedback.classList.add("my-2");
                        feedback.innerHTML = `Successfully bought ${val} share(s) of ${ticker}!`;
                        buyCard.append(feedback);
                    } else if (result.message == "Insufficient funds") {
                        const feedback = document.createElement('p');
                        feedback.classList.add("feedback");
                        feedback.classList.add("my-2");
                        feedback.innerHTML = "Insufficient funds!";
                        buyCard.append(feedback);
                    } else {
                        const feedback = document.createElement('p');
                        feedback.classList.add("feedback");
                        feedback.classList.add("my-2");
                        feedback.innerHTML = "Something went wrong! Please try again!";
                        buyCard.append(feedback);
                    }
                });
        }
    })
});