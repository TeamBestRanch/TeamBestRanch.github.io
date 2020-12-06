$(document).ready(function(){
    $("button").click(function(e){
        var data = $.parseJSON($(e.target).attr('data-button'));
        var restaurant_name = data.restName;
        var user_name = data.userName;
        var button_score = data.score;
        var update_score = "#setScore" + data.loop_index;


        $.ajax({
            data : {
                restaurant : restaurant_name,
                user : user_name,
                score : button_score
            },
            type : 'POST',
            url : '/process'
        })
        .done(function(data) {
            if (data.error) {
                alert("Hi Anonymous Nuggie! Please sign into your account to add your rating!🐥");
            } else {
                $(update_score).text("User Rating: " + data.avg);
            }
        });

        event.preventDefault();
    });
});