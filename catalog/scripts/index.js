$(function(context) {
    return function() {
      $('#num_pages').text(context.num_pages)
      $('#catalog').load('/catalog/index.inner/' + context.category_id + '/' + $('#page_number').text(),
        function() {
          $('#num_pages').text = context.num_pages
      })

      $( "#next_page" ).click(function() {
        var current_page = parseInt($('#page_number').text())
        var next_page = current_page + 1
        if(next_page > parseInt($('#num_pages').text()))
        {
          return;
        }
        else
        {
          $('#page_number').text(next_page)
          $('#catalog').load('/catalog/index.inner/' + context.category_id + '/' + next_page)
        }
      });

      $( "#prev_page" ).click(function() {
        var current_page = parseInt($('#page_number').text())
        var prev_page = current_page - 1
        if(prev_page <= 0)
        {
          return;
        }
        else
        {
          $('#page_number').text(prev_page)
          $('#catalog').load('/catalog/index.inner/' + context.category_id + '/' + prev_page)
        }
      });
    }


}(DMP_CONTEXT.get()))
