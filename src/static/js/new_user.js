const buttonRegister = document.getElementById("bt-register");

buttonRegister.addEventListener("click", function(e){
    e.preventDefault();
    const user_name = document.getElementById('user_name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const input_lengths = [user_name.length, email.length, password.length];
    if (input_lengths.some(item => item == 0)){
        alert("Existe campo em branco. Preencha todos os campos.");
        return false;
    }
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
        alert(`Usuário criado com sucesso!\n${response['message']}`);
        location.reload();
   })
   .fail(function(response, textStatus, msg){
        if ('msg'in response['responseJSON']){ 
            msg = response['responseJSON']['msg'];
            if (msg == 'Token has expired') {
                alert('Token expirou. Redirecionando para a tela de login.');
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
