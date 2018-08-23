$(document).ready(function () {
        let brand_id = window.location.href.split('/')[4];
        let car_id = window.location.href.split('/')[5];
        let csrf_token = jQuery("[name=csrfmiddlewaretoken]").val();
        let comments = $("#comments");

        $("#submit_search").click(function () {

        });

        $("#submit_filter").click(function () {
            let min_year = $('#id_min_year').val();
            let max_year = $('#id_max_year').val();
            let number_of_seats = $('#id_number_of_seats').val();
            let colour = $('#id_colour').val();
            let in_stock_only = $('#id_in_stock_only').prop('checked');
            let price = $('#id_price').val().split(/\D+/);
            let search_content = $("#search_content").attr("data-content");
            let data_dict = {
                'min_year': min_year,
                'max_year': max_year,
                'number_of_seats': number_of_seats,
                'colour': colour,
                'in_stock_only': in_stock_only,
                'min_price': price[1],
                'max_price': price[2]
            };
            if (search_content)
                data_dict['search_content'] = search_content;
            if (isNaN(brand_id))
                brand_id = 0;
            $.get(
                '/filter/' + brand_id + '/',
                data_dict,
                function (data) {
                    $("#brand_content").html(data)
                }
            );
        });

        $("#cancel_filter").click(function () {
            let search_content = $("#search_content").attr("data-content");
            let data_dict = {};
            if (isNaN(brand_id))
                brand_id = 0;
            if (search_content)
                data_dict['search_content'] = search_content;
            $.get(
                '/filter/' + brand_id + '/',
                data_dict,
                function (data) {
                    $("#brand_content").html(data);
                }
            );
        });

        $(comments).on("click", "#submit_comment", function () {
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
                }
            );
        });

        $(comments).on("click", "#save_ddit_comment", function () {
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
                }
            );
        });

        $(comments).on("click", "#cancel_edit_comment", function () {
            $.post(
                '/comment/',
                {
                    'flag': 'refresh',
                    'car_id': car_id,
                    'csrfmiddlewaretoken': csrf_token,
                },
                function (data) {
                    $("#comments").html(data);
                }
            );
        });

        $(comments).on("click", '.delete_comment', function () {
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
                }
            );
        });

        $(comments).on("click", '.edit_comment', function () {
            let comment_id = $(this).parents().attr("data-id");
            let old_comment_content = $(this).parents().children("#comment_content").text();
            let old_comment_rating = $(this).parents().children("#comment_rating").text();

            $.post(
                '/comment/',
                {
                    'flag': 'editing',
                    'car_id': car_id,
                    'content': old_comment_content,
                    'rating': old_comment_rating,
                    'comment_id': comment_id,
                    'csrfmiddlewaretoken': csrf_token,
                },
                function (data) {
                    $("#comments").html(data);
                }
            );
        });

        $("#users_cars").on("click", ".delete_car", function () {
            let car_id = $(this).attr("data-id");

            $.post(
                '/delete/car/',
                {
                    'car_id': car_id,
                    'csrfmiddlewaretoken': csrf_token,
                },
                function (data) {
                    $("#users_cars").html(data);
                }
            );
        });

        $("input").change(function () {
            preview(this);
        });

        function preview(input) {
            if (input.files) {
                let reader = new FileReader();
                reader.onload = function (e) {
                    $(input).parents(".preview").find("img#preview_image").attr('src', e.target.result);
                };
                reader.readAsDataURL(input.files[0]);
            }
        }
    }
);