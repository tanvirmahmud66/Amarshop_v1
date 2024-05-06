
// ------------------------------------------------------------------- product Details
var plusBtn = document.getElementById("plus")
var minusBtn = document.getElementById("minus")
var quantityElement = document.getElementById("q-input")
var addCartElement = document.getElementById("cart-dp")
var cartElement = document.getElementById("cart")

var q = 0
quantityElement.value = 0
minusBtn.addEventListener("click",function(){
    if (q > 0){
        q -= 1;
    }
    quantityElement.value = q
})
plusBtn.addEventListener("click",function(){
    q += 1
    quantityElement.value = q
})

addCartElement.addEventListener("click",function(){
    cartElement.innerText = q
})
