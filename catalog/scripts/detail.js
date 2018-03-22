$(function(context) {
    return function() {
      $('.thumbnail_image').mouseenter(function() {
        $("#product_image").attr("src",$(this).attr('src'))
      })
    }
}(DMP_CONTEXT.get()))
