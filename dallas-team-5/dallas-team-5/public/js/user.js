// INIT Button listeners
const form = document.getElementById("form");
form.addEventListener("submit", submitForm);

/*
    Function: Sends POST request to server using files the user chooses
    Params: event - the event initiated on the form
    Return: None
*/
function submitForm(e) {
    e.preventDefault();

    const name = document.getElementById("name");
    const files = document.getElementById("files");
    const formData = new FormData();

    console.log(files.files);
    if(files.files.length  === 0) { showToastFail() }

    else
    {
        formData.append("name", name.value);
        for(let i =0; i < files.files.length; i++) { formData.append("files", files.files[i]); }

        fetch("http://localhost:3000/upload_files", {
            method: 'POST',
            body: formData,
        })
        .then((res) => console.log(res))
        .catch((err) => ("Error occured", err));

        showToastSuccess()
    }
}

// Displays Toast if the files were uploaded
function showToastSuccess() 
{
    var x = document.getElementById("toast-message-success");
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

// Displays Toast if files could not be uploaded
function showToastFail() 
{
    var x = document.getElementById("toast-message-fail");
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}