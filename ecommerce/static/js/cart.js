

// -------------------------------------------------------------------cart
var updateBtns = document.getElementsByClassName("update-cart")
var cartBadge = document.getElementById("cart")


var cart = 0
cartBadge.innerText = cart;

for(var i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener("click",function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        cart += 1
        cartBadge.innerText = cart;
        console.log(cartBadge)
        console.log("product:",productId)
        console.log("action: ",action)
        console.log("user: ", user)
    })
}
