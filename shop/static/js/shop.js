function addbook(id){
     $.ajax({
            url:"/shop/add_in_bag",
            method:"POST",
            data:{book_id:id},
            success:function(response){
                console.log(response)
            }
     });
}


function createOrder(){
    order_items_list=[];
    $( ".item" ).each(function( index ) {
        quantity = $(this).find('input').val();
        book_id = $( this ).attr("id");
        cost = Number($(this).find('.item-cost').text())
        order_items_list.push(
            {"book_id":book_id,
             "quantity":quantity,
             "cost":cost
            }
        )
    });
    total =  Number($('#js-total').text())
    order = {"total":total}

    $.ajax({
        type: "POST",
        url: "/shop/order_from_bag",
        contentType : "application/json",
        dataType: "json",
        data:JSON.stringify({"order_items_list": order_items_list,
                            "order":order
        }),
        success: function(response){
            result = response.result
            if(result == 0){
                    $( "li" ).each(function( index ) {
                        $(this).remove()
                    })
                    $("#create-order").remove()
                    $("#block-total").remove()
                    $("#ajax-error").hide()
                    $("#ajax-success").html("Заказ создан успешно");
                    $("#ajax-success").show()

            }
            else{
                $("#ajax-success").hide()
                $("#ajax-error").html("Чтото пошло не так");
                $("#ajax-error").show()
            }
        }
    });
    console.log(order_items_list, order)
}


function costcalc(id){
    book = $('#'+id);
    price = $(book).find(".price").text()
    quantity = $(book).find("input").val()
    console.log(quantity*price);
    cost = quantity*price;
    if(cost >= 0){
        $(book).find('.item-cost').text(cost);
        total = 0;
        $('.item-cost').each(function(){
            total += Number($(this).text())
        })
        $('#js-total').text(total)
    }

}


$(document).ready(function(){
    total=0
    $('.item-cost').each(function(){
        total += Number($(this).text())
    })
    $('#js-total').text(total)
})