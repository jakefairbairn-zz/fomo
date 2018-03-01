$(function(context) {
  return function() {
    //Set the value of the hidden type field
    $("#id_type").val(context.type);

    //Assign classes based on model attributes
    console.log($('input'))
    $("#id_pid").parent().addClass("individual rental");
    $("#id_quantity").parent().addClass("bulk");
    $("#id_reorder_trigger").parent().addClass("bulk");
    $("#id_reorder_quantity").parent().addClass("bulk");
    $("#id_max_rental_days").parent().addClass("rental");
    $("#id_retire_date").parent().addClass("rental");

    //Hide/show fields based on what type of item is being edited
    if(context.type == 'IndividualProduct') {
      $(".bulk").hide();
      $(".rental").hide();
      $(".individual").show();
    }
    else if(context.type == 'BulkProduct') {
      $(".rental").hide();
      $(".individual").hide();
      $(".bulk").show();
    }
    else if(context.type == 'RentalProduct') {
      $(".individual").hide();
      $(".bulk").hide();
      $(".rental").show();
    }
  }
}(DMP_CONTEXT.get()))
