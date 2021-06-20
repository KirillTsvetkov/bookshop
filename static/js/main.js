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
    console.log(formData);
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

function delete_post(type,id){
    url = "/"+type+"/"+id;
    $.ajax({
        type: "DELETE",
        url: url,
        contentType : "application/json",
        dataType: "json",
        data:JSON.stringify(1),
        success: function(response){
            result = response.result
            if (result==0){
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