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
    .done(function(response){
        tokens = response['user']
        setCookie('premium_access', tokens['access'], 1);
        setCookie('premium_refresh', tokens['refresh'], 1);
        window.location.replace("/");
   })
    .fail(function(response, textStatus, msg){
        const error = response['responseJSON']['error'];
        alert(error);
    });
})

function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }
  
