function getFormData($form){
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

function create(){
    var formData = $("#js-form");
    formData=getFormData(formData);
    console.log(formData);
    $.ajax({
        type: "POST",
        url: "/genres",
        contentType : "application/json",
        dataType: "json",
        data:JSON.stringify(formData),
        success: function(response){
            console.log(response)
        }
    });
}