$( document ).ready(function() {
// Nothing here at the moment
});

$(document).on("click", "#componentEditButton", function () {
     var componentData = $(this).data('component').split(",");
     $(".modal-body #componentID").val(componentData[0].replace("[ObjectId('","").slice(0, -2));
     $(".modal-body #componentName").val(componentData[1].slice(2,-1));
     $(".modal-body #componentLocation").val(componentData[2].slice(2,-1));
     $(".modal-body #componentFootprint").val(componentData[3].slice(2,-1));
     $(".modal-body #componentAmount").val(componentData[4].slice(2,-1));
     $(".modal-body #componentDatasheet").val(componentData[5].slice(2,-1));
     $(".modal-body #componentEntryDate").val(componentData[6].slice(2,-1));
     $(".modal-body #componentUpdatedDate").val(componentData[7].slice(2,-1));
     $(".modal-body #componentComment").val(componentData[8].slice(2,-2));
});