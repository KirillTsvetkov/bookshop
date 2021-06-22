function getFormData($form){
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

function create(type){
    var formData = $("#js-form");
    url = "/"+type;
    formData=getFormData(formData);
    if(url == "/order_items"){
        formData = [formData]
    }
    console.log(formData, url);
    $.ajax({
        type: "POST",
        url: type,
        contentType : "application/json",
        dataType: "json",
        data:JSON.stringify(formData),
        success: function(response){
            result = response.result
            if (result==0){
                $("#ajax-error").hide()
                $("#ajax-success").html("Запись добавлена успешно");
                $("#ajax-success").show()
            }
            else{
                $("#ajax-success").hide()
                $("#ajax-error").html("Чтото пошло не так");
                $("#ajax-error").show()
            }
        }
    });
}

function update(type,id){
    var formData = $("#js-form");
    formData=getFormData(formData);
    console.log(formData);
    url = "/"+type+"/"+id;
    $.ajax({
        type: "PUT",
        url: url,
        contentType : "application/json",
        dataType: "json",
        data:JSON.stringify(formData),
        success: function(response){
            result = response.result
            if (result==0){
                $("#ajax-error").hide()
                $("#ajax-success").html("Изменения внесены успешно");
                $("#ajax-success").show()
            }
            else{
                $("#ajax-error").html("Чтото пошло не так");
                $("#ajax-error").show()
            }
        }
    });
}

function delete_post(type,id,e){
    row = $(event.target).closest('tr');
    console.log(row);
    url = "/"+type+"/"+id;
    $.ajax({
        type: "DELETE",
        url: url,
        contentType : "application/json",
        dataType: "json",
        data:JSON.stringify(1),
        success: function(response){
            result = response.result
            console.log(response)
            if (result==0){
                $(row).remove()
                $("#ajax-error").hide()
                $("#ajax-success").html("Изменения внесены успешно");
                $("#ajax-success").show()
            }
            else{
                $("#ajax-success").hide()
                $("#ajax-error").html("Чтото пошло не так");
                $("#ajax-error").show()
            }
        }
    });
}

function addbook(id){
     $.ajax({
            url:"/add_in_bag",
            method:"POST",
            data:{book_id:id},
            success:function(response){
                console.log(response)
            }
     });
}


function createOrder(){
    order_items_list=[];
    $( "li" ).each(function( index ) {
        quantity = $(this).find('input').val();
        book_id = $( this ).attr("id");
        order_items_list.push(
            {"book_id":book_id,
             "quantity":quantity
            }
        )
    });
    console.log(order_items_list)
}


function total(id,e){
    book = $('#'+id);
    price = $(book).find(".price").text()
    quantity = $(book).find("input").val()
    console.log(quantity*price);
    cost = quantity*price;
    if(cost >= 0){
        $(book).find('.cost').text("Цена позиции: " + cost + " р.");
    }
}