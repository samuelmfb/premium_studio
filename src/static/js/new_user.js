const buttonRegister = document.getElementById("bt-register");

buttonRegister.addEventListener("click", function(e){
    e.preventDefault();
    const user_name = document.getElementById('user_name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    data = {
        "user_name": user_name,
        "email" : email,
        "password" : password
    }
    $.ajax({
        url : "/api/v1/auth/register",
        type : 'post',
        data : JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
   })
    .done(function(response, msg){
        console.log(response,msg);
        alert('Usuário criado com sucesso!');
        location.reload();
   })
   .fail(function(response, textStatus, msg){
        if ('msg'in response['responseJSON']){ 
            msg = response['responseJSON']['msg'];
            if (msg == 'Token has expired') {
                alert(msg);
                window.location.replace("/login");
            };
        } 
        if ('error'in response['responseJSON']){
            const error = response['responseJSON']['error'];
            if (error) {
                alert(error);
            };
        }
    });
})