function addToCart(id, name, price) {
    fetch("/api/cart", {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        let carts = document.getElementsByClassName('cart-counter');
        for (let c of carts)
            c.innerText = data.total_quantity;
    });
}

function updateCart(id, obj) {
    obj.disabled = true;
    fetch(`/api/cart/${id}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        obj.disabled = false;
        let carts = document.getElementsByClassName('cart-counter');
        for (let c of carts)
            c.innerText = data.total_quantity;

        let amounts = document.getElementsByClassName('cart-amount');
        for (let c of amounts)
            c.innerText = data.total_amount.toLocaleString("en");
    });
}

function deleteCart(id, obj) {
    if (confirm("Bạn chắc chắn xóa?") === true) {
        obj.disabled = true;
        fetch(`/api/cart/${id}`, {
            method: "delete"
        }).then(function(res) {
            return res.json();
        }).then(function(data) {
            obj.disabled = false;
            let carts = document.getElementsByClassName('cart-counter');
            for (let c of carts)
                c.innerText = data.total_quantity;

            let amounts = document.getElementsByClassName('cart-amount');
            for (let c of amounts)
                c.innerText = data.total_amount.toLocaleString("en");

            let t = document.getElementById(`product${id}`);
            t.style.display = "none";
        });
    }
}

function pay() {
    if (confirm("Bạn chắc chắn thanh toán?") === true) {
        fetch("/api/pay", {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.status === 200)
                location.reload();
            else
                alert(data.err_msg)
        })
    }
}