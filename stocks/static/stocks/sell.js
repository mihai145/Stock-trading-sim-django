document.addEventListener('DOMContentLoaded', function () {
    document.querySelector("#sell-button").addEventListener('click', () => {
        ///clearing any previous feedback
        const prevFeedback = document.querySelector('.feedback');
        if (prevFeedback) {
            prevFeedback.remove();
        }

        const sellCard = document.querySelector("#sell-card");

        const amountField = document.querySelector("#sold-stocks");
        const val = amountField.value;
        amountField.value = '';

        if (amountField <= 0) {
            const feedback = document.createElement('p');
            feedback.classList.add("feedback");
            feedback.classList.add("my-2");
            feedback.innerHTML = `You cannout sell less than one share!`;
            buyCard.append(feedback);
        } else {
            const ticker = document.querySelector("#ticker").innerHTML;
            const pricePerShare = document.querySelector("#adjusted-sell").innerHTML;

            fetch(`/sell/${ticker}`, {
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
                        const newOwned = parseInt(owned.innerHTML) - parseInt(val);
                        owned.innerHTML = newOwned.toString();

                        const feedback = document.createElement('p');
                        feedback.classList.add("feedback");
                        feedback.classList.add("my-2");
                        feedback.innerHTML = `Successfully sold ${val} share(s) of ${ticker}!`;
                        sellCard.append(feedback);
                    } else if (result.message == "Insufficient shares owned") {
                        const feedback = document.createElement('p');
                        feedback.classList.add("feedback");
                        feedback.classList.add("my-2");
                        feedback.innerHTML = "Insufficient shares owned!";
                        sellCard.append(feedback);
                    } else {
                        const feedback = document.createElement('p');
                        feedback.classList.add("feedback");
                        feedback.classList.add("my-2");
                        feedback.innerHTML = "Something went wrong! Please try again!";
                        sellCard.append(feedback);
                    }
                });
        }
    })
});