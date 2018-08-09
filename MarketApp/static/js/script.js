$(document).ready(function () {

    $("#filterSubmit").click(function () {
        let min_year = $('#id_min_year').val();
        let max_year = $('#id_max_year').val();
        let number_of_seats = $('#id_number_of_seats').val();
        let colour = $('#id_colour').val();
        let in_stock_only = $('#id_in_stock_only').prop('checked');
        let price = $('#id_price').val().split(/\D+/);
        let brand_id = window.location.href.split('/')[window.location.href.split('/').length - 2];

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
});