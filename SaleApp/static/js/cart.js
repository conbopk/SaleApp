function addToCart(id, name, price) {
    event.preventDefault()

    fetch('/api/add-cart',
    {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)

        let counter = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < counter.length; i++)
            counter[i].innerText = data.total_quantity
    }).catch(function(err) {
        console.error(err)
    })
}

function pay(){
    if (confirm('Confirm Payment') == true) {
        fetch('/api/pay',
        {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if(data.code == 200)
                location.reload()
        }).catch(err => console.error(err))
    }
}


function updateCart(id, obj) {
    fetch('/api/update-cart', {
        method: 'PUT',
        body: JSON.stringify({
            'id': id,
            'quantity': parseInt(obj.value)
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let counter = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < counter.length; i++)
            counter[i].innerText = data.total_quantity

        let amount = document.getElementById('total-amount')
        amount.innerText = new Intl.NumberFormat().format(data.total_amount)
    })
}


function deleteCart(id) {
    if (confirm("Are you sure you want to delete this product?") == true) {
        fetch('/app/delete-cart/' + id, {
            method: 'delete',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            let counter = document.getElementsByClassName('cart-counter')
            for (let i = 0; i < counter.length; i++)
                counter[i].innerText = data.total_quantity

            let amount = document.getElementById('total-amount')
            amount.innerText = new Intl.NumberFormat().format(data.total_amount)

            let e = document.getElementById("product" + id)
            e.style.display = "none"
        }).catch(err => console.error(err))
    }
}


function addComment(productId) {
    let content = document.getElementById('commentId')
    if (content !== null) {
        fetch('/api/comments', {
            method: 'post',
            body: JSON.stringify({
                'product_id': productId,
                'content': content.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data.status == 201) {
                let comment = data.comment

                let area = document.getElementById('commentArea')

                area.innerHTML = `
                    <div class="row">
                        <div class="col-md-1 col-xs-4">
                            <img src="${comment.user.avatar}" class="img-fluid rounded-circle" alt="demo" />
                        </div>
                        <div class="col-md-11 col-xs-8">
                            <p>${comment.content}</p>
                            <p><em>${moment(comment.created_date).fromNow()}</em></p>
                        </div>
                    </div>
                ` + area.innerHTML

            } else if (data.status == 404)
                alert(data.err_msg)
        })
    }
}

