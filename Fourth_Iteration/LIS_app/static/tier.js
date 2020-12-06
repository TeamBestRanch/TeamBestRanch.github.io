var i = 0;
$(document).ready(function(){
    $("button").click(function(e){
        var data = $.parseJSON($(e.target).attr('data-button'));
        var user_name = data.userName;
        var UserClickCounter = i+1;

        $.ajax({
            data : {
                UserCounter : UserClickCounter,
                user : user_name,
            },
            type : 'POST',
            url : '/TierList'
        })
        .done(function(data) {
            if (data.error) {
                alert("Hi Anonymous Nuggie! Please sign into your account to add your rating!🐥");
            } 
        });

        event.preventDefault();
    });
});