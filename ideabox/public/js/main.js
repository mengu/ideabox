var ideabox = {
  // Function to toggle the status of a task
  toggleComplete: function() {
    var completed = !!$(this).attr('checked');
    var image = completed ? 'check.png' : 'undone.png';
    
    $.post('/tasks/complete/'+this.id, {"completed": completed});
    
    toast = $('#completed_'+this.id).children('img')[0].src = '/img/' + image;
  },

  // Function to toggle/expand a collapsed task
  expandTask: function(e) {
    // TODO write this

  }
}


$(document).ready(function(){
    // TODO use event delegation for the task lists

    // TODO this will select all checkboxes where this code runs, should be more specific
    $("input[type='checkbox']").click(ideabox.toggleComplete);
    
    // Show the full description when a task is expanded
    $(".expandTask").click(ideabox.expandTask);  
    
    // TODO describe this
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
        $.post("/projects/"+project_id+"/users/new", {"username": username}, function(data){
            $(".user-list").append('<div class="line">\
                <div class="unit size1of5"><a href="/users/show/'+data.id+'">'+data.firstname+' '+data.lastname+'</a></div>\
                <div class="unit size1of3"><a href="/projects/deleteuser/'+data.id+'">Delete</a></div>\
                </div>');
            $("#username-box").val("");
        }, "json");
        return false;
    });

});

