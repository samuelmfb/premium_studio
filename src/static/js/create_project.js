const button = document.getElementById("bt-submit");

$(document).ready(function() {
    login_validation();
})
button.addEventListener("click", function(e){
    e.preventDefault();
    const name = document.getElementById('name').value;
    const full_value = document.getElementById('full_value').value;
    const producer = Number(document.getElementById('producer').value);
    const customer = Number(document.getElementById('customer').value);
    const description = document.getElementById('description').value;
    data = {
        "name": name,
        "full_value" : full_value,
        "id_producer" : producer,
        "id_customer" : customer,
        "description" : description,
    }
    $.ajax({
        url : "/api/v1/project",
        type : 'post',
        data : JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        headers: {"Authorization": "Bearer " + getCookie('premium_access')}
   })
    .done(function(response, msg){
        console.log(response,msg);
        alert('Registro adicionado com sucesso!');
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

function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
        }
    }
    return "";
    }

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