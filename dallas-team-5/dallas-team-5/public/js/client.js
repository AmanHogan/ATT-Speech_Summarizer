/* Loads jobs page on button click */
function goToJobPage(){
    window.open("http://localhost:3000/jobs", "self");
}

/*
    Function: Shows loading icon on press, and then shows a random number for customer PIN,
    and then disappears.
    Params: None
    Return: None
*/
function showCustomerPin(){
    
    let showCustomerPinBtn = document.getElementById("client-pin-button");
    let loadingIcon = document.getElementById("loading-icon");
    let showCustomerButtonString = showCustomerPinBtn.innerHTML;

    showCustomerPinBtn.innerHTML = "";
    loadingIcon.style.visibility="visible";
    showCustomerPinBtn.appendChild(loadingIcon);

    setTimeout(() => {
        loadingIcon.style.visibility="hidden";
        showCustomerPinBtn.innerHTML = String(Math.round(Math.random() * 1000) + 1);
    }, "2000");


    setTimeout(() => {
        showCustomerPinBtn = document.getElementById("client-pin-button");
        showCustomerPinBtn.innerHTML = showCustomerButtonString;
    }, "5000");
}


