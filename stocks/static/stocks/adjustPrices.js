document.addEventListener('DOMContentLoaded', function () {
    let currentPrice = parseInt(document.querySelector("#price").innerHTML);
    document.querySelector("#adjusted-buy").innerHTML = currentPrice + 1;
    document.querySelector("#adjusted-sell").innerHTML = currentPrice;
});