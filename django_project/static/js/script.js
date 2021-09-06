$('#likeForm').submit(function (e) { 
    e.preventDefault();

    $.ajax({
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        data: $(this).serialize(),
        dataType: "json",
        success: function (response) {
            let prevLikesNumber = Number($('.likesNumber').html())

            let currentlikesNumber = response.liked ? (prevLikesNumber + 1) : (prevLikesNumber - 1);
            let iconColor = response.liked ? 'red' : 'currentColor';

            $('.like-icon').attr('fill', iconColor);
            $('.likesNumber').html(currentlikesNumber);
        }
    });
});
