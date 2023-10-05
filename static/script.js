var name_stn = "";


$(".stn").click(function (){

    name_stn= $(this).attr("id");
    console.log("global var: "+name_stn); 
})



function setFrom() {
    
    $("#from").val(name_stn);
    // console.log("from var: "+name_stn);  <-- for debugging
  
}

function setTo() {
   
    $("#to").val(name_stn);
    // console.log("to var: "+name_stn);  <-- for debugging
   
}


// document.getElementById("bookingForm").onsubmit = function(event) 
// {
//    // Prevent the form from submitting immediately
// event.preventDefault();

//     // Get the selected date value from the input field  
// const selectedDate = new Date(document.getElementById("dt").value);

//     // Get the current date
// const currentDate = new Date();

//     // Set the time of the current date to midnight (to compare dates without time)
// currentDate.setHours(0, 0, 0, 0);

//     // Compare the selected date with the current date
// if (selectedDate < currentDate) {
//       // If the selected date is in the past, show an error message
// alert("Please select a present or future date.");
// } 
// else 
// {
//       // If the selected date is valid, you can proceed with form submission
//       document.getElementById("bookingForm").submit();
//     }
// };


