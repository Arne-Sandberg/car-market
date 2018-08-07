$("#filterSubmit").click(function () {
    let min_year = $('#minYearNumber').val();
    let max_year = $('#maxYearNumber').val();
    let number_of_seats = $('#seatNumber').val();
    let colour = $('#colourSelect').val();
    let is_in_stock = $('#instockCheckbox').prop('checked');
    let brand_name = $('#brandName').text();

    $.ajax({
        url: '/filter/',
        data: {
            'min_year': min_year,
            'max_year': max_year,
            'number_of_seats': number_of_seats,
            'colour': colour,
            'is_in_stock': is_in_stock,
            'brand_name': brand_name,
        },
        dataType: 'json',
        success: function (data) {

        }
    });

});