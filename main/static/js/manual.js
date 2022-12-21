$(document).ready(function() {

    $('th').each(function (col) {
        $(this).hover(
                function () {
                    $(this).addClass('focus');
                },
                function () {
                    $(this).removeClass('focus');
                }
        );
        $(this).click(function () {
            if ($(this).is('.asc')) {
                $(this).removeClass('asc');
                $(this).addClass('desc selected');
                $(this).children(1).remove()
                $(this).append(
                    '<i class="bi bi-sort-down"></i>'
                )

                sortOrder = -1;
            } else {
                $(this).addClass('asc selected');
                $(this).removeClass('desc');
                $(this).children(1).remove()
                $(this).append(
                    '<i class="bi bi-sort-up"></i>'
                )
                sortOrder = 1;
            }
            $(this).siblings().removeClass('asc selected');
            $(this).siblings().removeClass('desc selected');
            var arrData = $('table').find('tbody >tr:has(td)').get();
            arrData.sort(function (a, b) {
                var val1 = $(a).children('td').eq(col).text().toUpperCase();
                var val2 = $(b).children('td').eq(col).text().toUpperCase();
                if ($.isNumeric(val1) && $.isNumeric(val2))
                    return sortOrder == 1 ? val1 - val2 : val2 - val1;
                else
                    return (val1 < val2) ? -sortOrder : (val1 > val2) ? sortOrder : 0;
            });
            $.each(arrData, function (index, row) {
                $('tbody').append(row);
            });
        });
    });


    $('#reset').on('click', function(){
        $(':input','#filter_form')
  .not(':button, :submit, :reset, :hidden')
  .val('')
  .removeAttr('checked')
  .removeAttr('selected');
    })

});