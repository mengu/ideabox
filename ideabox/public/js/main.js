$(document).ready(function(){
    $("input[type='checkbox']").click(function(){
       var completed = $(this).attr('checked') ? true : false;
       var completedImage = completed ? '<img src="../../img/check.png" border="0" />' : '<img src="../../img/undone.png" border="0" />';
       $.post('/tasks/complete/'+this.id, {"completed": completed});
       $("#completed_"+this.id).html(completedImage);
    });
    $("input").attr("checked").css("background", "#000");
});

