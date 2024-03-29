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

$(document).on("click", "#componentRemoveButton", function () {
     var postId = $(".modal-body #componentID").val();

     $.post("/remove", {id: postId}, function(data) {
        if(data['n']){
            displayModal("componentEditModal", false, true, 2000, "Component has been removed.");
        }else if (!data['n']){
            displayModal("componentEditModal", true, false, 0, "A database entry with that ID cannot be found.");
        }else{
            displayModal("componentEditModal", true, false, 0, data);
            console.log(data);
        }
      });
});

// Datasheet button on add component modal

// File lines
const uploadHTML = "<input type=\"file\" name=\"datasheetUpload\" id=\"newComponentDatasheet\" class=\"form-control\" accept=\".pdf,.doc,.docx,.txt,.rtf\">";
const linkHTML = "<input type=\"text\" name=\"datasheetLink\" id=\"newComponentDatasheet\" class=\"form-control\">";

$(document).on('change', 'input:radio[id^="datasheetToggle_"]', function (event) {
    if(event.target.id == "datasheetToggle_upload")
        $("#datasheetMethod").html(uploadHTML);
    else
        $("#datasheetMethod").html(linkHTML);
});

// Add component form
$('#addComponentForm').submit(function(e) {

    e.preventDefault();
    var formData = new FormData(this);
    //formData.append('file', $('#datasheetUpload').prop('files')[0]);

    $.ajax({
        type : 'POST',
        url : '/add',
        data : formData,
        cache: false,
        contentType: false,
        processData: false
    })
    .done(function(data) {
       if (data == "True"){
        displayModal("componentAddModal", false, true, 2000, "Component has been added.");
       }else{
        displayModal("componentAddModal", true, false, 0, data);
       }
    });
});

// Edit component form
$('#editComponentForm').submit(function(e) {

    e.preventDefault();

    var formData = $('#editComponentForm').serialize();

    $.ajax({
        type : 'POST',
        url : '/update',
        data : formData
    })
    .done(function(data) {
       if (data == "True"){
        displayModal("componentEditModal", false, true, 2000, "Component has been updated.");
       }else{
        displayModal("componentEditModal", true, false, 0, data);
       }
    });
});


function displayModal(currentModal, isError, isTimeout, timeoutLength, modalMessage){

    var successModal = new bootstrap.Modal(document.getElementById('successModal'));
    var errorModal = new bootstrap.Modal(document.getElementById('errorModal'));

    var currentModalElement = document.getElementById(currentModal);
    var current = bootstrap.Modal.getInstance(currentModalElement);

    if (isError){
        errorModal.show();
        $("#errorModalBody #modalErrorMessage").html(modalMessage);
        if (isTimeout){
            setTimeout(function(){
                    errorModal.hide();
                }, timeoutLength);
        }
    }else{
        current.hide();
        $("#componentTable").load(location.href+" #componentTable>*","");
        successModal.show();
        $("#successModalBody #modalSuccessMessage").html(modalMessage);
        if (isTimeout){
            setTimeout(function(){
                    successModal.hide();
                }, timeoutLength);
        }
    }
}