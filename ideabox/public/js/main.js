$(document).ready(function(){
    $("input[type='checkbox']").click(function(){
       var completed = $(this).attr('checked') ? true : false;
       var completedImage = completed ? '<img src="../../img/check.png" border="0" />' : '<img src="../../img/undone.png" border="0" />';
       $.post('/tasks/complete/'+this.id, {"completed": completed});
       $("#completed_"+this.id).html(completedImage);
    });

    if (($("input").size > 0) && ($("input").attr("checked").size > 0)) {
        $("input").attr("checked").css("background", "#000");
    }

    // auto complete
    if (jQuery.isFunction(jQuery.fn.autocomplete)) {
        $("#username-box").autocomplete("/users/find");
    }
    // add user
    $("#add-user").click(function(){
        var project_id = $("#project_id").val();
        var username = $("#username-box").val();
        $.post("/projects/newuser/"+project_id, {"username": username}, function(data){
            $(".user-list").append('<div class="line">\
                <div class="unit size1of5"><a href="/users/show/'+data.id+'">'+data.firstname+' '+data.lastname+'</a></div>\
                <div class="unit size1of3"><a href="/projects/deleteuser/'+data.id+'">Delete</a></div>\
                </div>');
            $("#username-box").val("");
        });
        return false;
    });

});

