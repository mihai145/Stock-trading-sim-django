document.addEventListener('DOMContentLoaded', function () {
    document.querySelector("#invest-button").addEventListener('click', () => {
        ///clearing any previous feedback
        const prevFeedback = document.querySelector('.feedback');
        if (prevFeedback) {
            prevFeedback.remove();
        }

        const investCard = document.querySelector("#invest-card");

        const amountField = document.querySelector("#amount-invested");
        const val = amountField.value;
        amountField.value = '';

        if (val > 0) {
            fetch('/invest', {
                    method: 'POST',
                    body: JSON.stringify({
                        amount: val,
                    })
                })
                .then(response => response.json())
                .then(result => {
                    if (result.message == "OK") {
                        const capital = document.querySelector("#capital");
                        const newCapital = parseInt(capital.innerHTML) + parseInt(val);
                        capital.innerHTML = newCapital.toString();

                        const feedback = document.createElement('p');
                        feedback.classList.add("feedback");
                        feedback.classList.add("my-2");
                        feedback.innerHTML = `Successfully added ${val}$ to your account!`;
                        investCard.append(feedback);
                    } else {
                        const feedback = document.createElement('p');
                        feedback.classList.add("feedback");
                        feedback.classList.add("my-2");
                        feedback.innerHTML = "Something went wrong! Please enter a valid amount and try again!";
                        investCard.append(feedback);
                    }
                });
        } else {
            const feedback = document.createElement('p');
            feedback.classList.add("feedback");
            feedback.classList.add("my-2");
            feedback.innerHTML = "You can only add amounts of at least 1$";
            investCard.append(feedback);
        }
    });
});