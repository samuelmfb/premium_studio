const loginButton = document.getElementById("bt-login");

loginButton.addEventListener("click", function(e){
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    data = {
        "email" : email,
        "password" : password
    }
    $.ajax({
        url : "/api/v1/auth/login",
        type : 'post',
        data : JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
   })
    .done(function(msg){
        window.location.replace("/");
   })
    .fail(function(response, textStatus, msg){
        const error = response['responseJSON']['error'];
        alert(error);
    });
})