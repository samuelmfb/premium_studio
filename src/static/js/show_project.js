$(document).ready(function() {
    login_validation();
})
function login_validation() {
    if (getCookie('premium_access') == "") {
        alert('Usuário não logado. Redirecionando para a tela de login.');
                window.location.replace("/login")
    }
    $.ajax({
        url : "/api/v1/auth/me",
        type : 'get',
        contentType: "application/json; charset=utf-8",
        async: false, 
        headers: {"Authorization": "Bearer " + getCookie('premium_access')}
   })
    .done(function(response, msg, data){
        console.log(response, msg);
        
   })
   .fail(function(response, textStatus, msg){
    console.log(response, msg);
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
}