$(document).ready(function () {
    let brand_id = window.location.href.split('/')[4];
    let car_id = window.location.href.split('/')[5];
    let csrf_token = jQuery("[name=csrfmiddlewaretoken]").val();

    function refreshUserComment() {
        $.post(
            '/comment/edit/',
            {
                'flag': 'refresh',
                'csrfmiddlewaretoken': csrf_token,
            },
            function (data) {
                $("#user_comment").html(data);
            }
        );
    }

    $("#submitFilter").click(function () {
        let min_year = $('#id_min_year').val();
        let max_year = $('#id_max_year').val();
        let number_of_seats = $('#id_number_of_seats').val();
        let colour = $('#id_colour').val();
        let in_stock_only = $('#id_in_stock_only').prop('checked');
        let price = $('#id_price').val().split(/\D+/);

        $.get(
            '/filter/' + brand_id + '/',
            {
                'min_year': min_year,
                'max_year': max_year,
                'number_of_seats': number_of_seats,
                'colour': colour,
                'in_stock_only': in_stock_only,
                'min_price': price[1],
                'max_price': price[2]
            },
            function (data) {
                $("#brand_content").html(data)
            }
        );
    });

    $("#cancelFilter").click(function () {
        $.get(
            '/filter/' + brand_id + '/',
            function (data) {
                $("#brand_content").html(data);
            }
        );
    });

    $("#comment").on("click", "#submitComment", function () {
        let new_comment_content = $('#id_content').val();
        let new_comment_rating = $('#id_rating').val();

        $.post(
            '/comment/',
            {
                'flag': 'create',
                'content': new_comment_content,
                'rating': new_comment_rating,
                'car_id': car_id,
                'csrfmiddlewaretoken': csrf_token,
            },
            function (data) {
                $("#comments").html(data);
                refreshUserComment();
            }
        );
    });

    $("#comment").on("click", "#saveEditComment", function () {
        let new_comment_content = $('#id_content').val();
        let new_comment_rating = $('#id_rating').val();
        let comment_id = $(this).parents().attr("data-id");

        $.post(
            '/comment/',
            {
                'flag': 'edit',
                'comment_id': comment_id,
                'content': new_comment_content,
                'rating': new_comment_rating,
                'car_id': car_id,
                'csrfmiddlewaretoken': csrf_token,
            },
            function (data) {
                $("#comments").html(data);
                refreshUserComment();
            }
        );
    });


    $("#comment").on("click", "#cancelEditComment", function () {
        $.post(
            '/comment/',
            {
                'flag': 'refresh',
                'car_id': car_id,
                'csrfmiddlewaretoken': csrf_token,
            },
            function (data) {
                $("#comments").html(data);
                refreshUserComment();
            }
        );
    });

    $("#comments_content").on("click", 'a.deleteComment', function () {
        let comment_id = $(this).parents().attr("data-id");

        $.post(
            '/comment/',
            {
                'flag': 'delete',
                'comment_id': comment_id,
                'car_id': car_id,
                'csrfmiddlewaretoken': csrf_token,
            },
            function (data) {
                $("#comments").html(data);
                refreshUserComment();
            }
        );
    });


    $("#comments_content").on("click", 'a.editComment', function () {
        let comment_id = $(this).parents().attr("data-id");
        let old_comment_content = $(this).parents().children("#comment_content").text();
        let old_comment_rating = $(this).parents().children("#comment_rating").text();

        $.post(
            '/comment/',
            {
                'flag': 'editing',
                'car_id': car_id,
                'comment_id': comment_id,
                'csrfmiddlewaretoken': csrf_token,
            },
            function (data) {
                $("#comments").html(data);
            }
        );

        $.post(
            '/comment/edit/',
            {
                'flag': 'edit',
                'comment_id': comment_id,
                'content': old_comment_content,
                'rating': old_comment_rating,
                'csrfmiddlewaretoken': csrf_token,
            },
            function (data) {
                $("#user_comment").html(data);
            }
        );
    });
});