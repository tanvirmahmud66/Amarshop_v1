

// -------------------------------------------------------------------cart
var updateBtns = document.getElementsByClassName("update-cart")
// var cartBadge = document.getElementById("cart")


// var cart = 0
// cartBadge.innerText = cart;

for(var i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener("click",function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        var quantity = this.dataset.quantity? this.dataset.quantity : 1;
        // cart += 1
        // cartBadge.innerText = cart;
        if (user ==="AnonymousUser"){
            console.log("User is not authenticated")
        }else{
            updateUserOrder(productId,action,quantity)
        }
    })
}

function updateUserOrder(productId,action,quantity){
    var url = '/update-item/'
    fetch(url,{
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId':productId,'quantity':quantity,'action':action})
    }).then((response)=>{
        return response.json()
    }).then((data)=>{
        console.log(data)
        location.reload()
    })
}
