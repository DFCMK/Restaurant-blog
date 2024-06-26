$(document).ready(function () {
    $(document).on('click', '.thumbaction', function (e) {
        e.preventDefault();
        console.log("Thumb button clicked");
        var postid = $(this).closest('.thumb-container').find('#thumbs').data('value');
        var button = $(this).attr("value");
        $.ajax({
            type: 'POST',
            url: thumbsUrl,
            data: {
                postid: postid,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action: 'thumbs',
                button: button,
            },
            success: function (json) {
                if (json.length < 1 || json == undefined) {
                }
                $("#up").text(json['up']);
                $("#down").text(json['down']);
                $("svg").removeClass("thumb-active");
                if (json['remove'] == 'none') {
                    $("#" + button).removeClass("thumb-active");
                } else {
                    $("#" + button).addClass("thumb-active");
                }
            },
            error: function (xhr, errmsg, err) {
            }
        });
    });
});