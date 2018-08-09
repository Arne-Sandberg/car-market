$(document).ready(function () {
    $("#filterSubmit").click(function () {
        let brand_name = $('#brandName').text();
        let min_year = $('#id_min_year').val();
        let max_year = $('#id_max_year').val();
        let number_of_seats = $('#id_number_of_seats').val();
        let colour = $('#id_colour').val();
        let in_stock_only = $('#id_in_stock_only').prop('checked');
        let price = $('#id_price').val().split(/\D+/);

        $.ajax({
            url: '/filter/',
            data: {
                'brand_name': brand_name,
                'min_year': min_year,
                'max_year': max_year,
                'number_of_seats': number_of_seats,
                'colour': colour,
                'in_stock_only': in_stock_only,
                'min_price': price[1],
                'max_price': price[2]
            },
            dataType: 'json',
            success: function () {
                alert('ok')
            }
        });

    });
});