
// ------------------------------------------------------------------- product Details
var plusBtn = document.getElementById("plus")
var minusBtn = document.getElementById("minus")
var qInputElement = document.getElementById("q-input")
var addCartElement = document.getElementById("cart-dp")

var q = 1
qInputElement.value = 1
minusBtn.addEventListener("click",function(){
    if (q > 1){
        q -= 1;
    }
    qInputElement.value = q
    addCartElement.dataset.quantity = q
    console.log("dataset",addCartElement.dataset.quantity)
})
plusBtn.addEventListener("click",function(){
    q += 1
    qInputElement.value = q
    addCartElement.dataset.quantity = q
    console.log("dataset", addCartElement.dataset.quantity)
})

addCartElement.addEventListener("click",function(){
    console.log(this.dataset.quantity)
})



