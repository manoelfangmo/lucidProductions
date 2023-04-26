oneStarReview = document.getElementById("oneStar")
twoStarReview = document.getElementById("twoStar")
threeStarReview = document.getElementById("threeStar")
fourStarReview = document.getElementById("fourStar")
fiveStarReview = document.getElementById("fiveStar")

oneStarReview.addEventListener("click", function () {
    oneStarReview.classList.add("checked")
    twoStarReview.classList.remove("checked")
    threeStarReview.classList.remove("checked")
    fourStarReview.classList.remove("checked")
    fiveStarReview.classList.remove("checked")
    document.querySelector('[name="review_rating"]').value = 1


});
twoStarReview.addEventListener("click", function () {
    oneStarReview.classList.add("checked")
    twoStarReview.classList.add("checked")
    threeStarReview.classList.remove("checked")
    fourStarReview.classList.remove("checked")
    fiveStarReview.classList.remove("checked")
    document.querySelector('[name="review_rating"]').value = 2


});
threeStarReview.addEventListener("click", function () {
    oneStarReview.classList.add("checked")
    twoStarReview.classList.add("checked")
    threeStarReview.classList.add("checked")
    fourStarReview.classList.remove("checked")
    fiveStarReview.classList.remove("checked")
    document.querySelector('[name="review_rating"]').value = 3


});

fourStarReview.addEventListener("click", function () {
    oneStarReview.classList.add("checked")
    twoStarReview.classList.add("checked")
    threeStarReview.classList.add("checked")
    fourStarReview.classList.add("checked")
    fiveStarReview.classList.remove("checked")
    document.querySelector('[name="review_rating"]').value = 4


});

fiveStarReview.addEventListener("click", function () {
    oneStarReview.classList.add("checked")
    twoStarReview.classList.add("checked")
    threeStarReview.classList.add("checked")
    fourStarReview.classList.add("checked")
    fiveStarReview.classList.add("checked")
    document.querySelector('[name="review_rating"]').value = 5


});