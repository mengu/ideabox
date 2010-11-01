var ideabox = {
  // Function to toggle the status of a task
  toggleComplete: function() {
    var completed = !!$(this).attr('checked');
    var image = completed ? 'check.png' : 'undone.png';
    
    $.post('/tasks/complete/'+this.id, {"completed": completed});
    
    $('#completed_'+this.id).children('img')[0].src = '/img/' + image;
  },

  // Function to toggle/expand a collapsed task
  expandTask: function(e) {
    e.preventDefault();
    $(this).prev('span').hide();
    $(this).hide();
    $(this).next('span').show();
  },

  addUser: function() {
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
  }
}


$(document).ready(function(){
  // Toggle completed status on projects/show
  $("input[type='checkbox'].toggleStatus").click(ideabox.toggleComplete);

  // Show the full description when a task is expanded
  $(".expandTask").click(ideabox.expandTask);

  // TODO implement a confirmation for delete
  // $('.deleteClass').click(ideabox.confirmDelete);

  // TODO describe this
  if (($("input").size > 0) && ($("input").attr("checked").size > 0)) {
    $("input").attr("checked").css("background", "#000");
  }

  // auto complete
  if (jQuery.isFunction(jQuery.fn.autocomplete)) {
    $("#username-box").autocomplete("/users/find");
  }

  // add user
  $("#add-user").click(ideabox.addUser);

});

