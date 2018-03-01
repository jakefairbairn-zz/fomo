$(function(context) {

  // Assign classes based on model attributes
  $("#id_pid").parent().addClass("individual rental");
  $("#id_quantity").parent().addClass("bulk");
  $("#id_reorder_trigger").parent().addClass("bulk");
  $("#id_reorder_quantity").parent().addClass("bulk");
  $("#id_max_rental_days").parent().addClass("rental");
  $("#id_retire_date").parent().addClass("rental");

  //Call the function to set the initial form
  changeForm();

  // Hide/show fields based on what type of item is being created
  $('#id_type').change(function() {
    changeForm();
  });
});

function changeForm() {
  if($('#id_type').val() == 'IndividualProduct') {
    $(".bulk").hide(1000);
    $(".rental").hide(1000);
    $(".individual").show(1000);
  }
  else if($('#id_type').val() == 'BulkProduct') {
    $(".rental").hide(1000);
    $(".individual").hide(1000);
    $(".bulk").show(1000);
  }
  else if($('#id_type').val() == 'RentalProduct') {
    $(".bulk").hide(1000);
    $(".individual").hide(1000);
    $(".rental").show(1000);
  }
}
