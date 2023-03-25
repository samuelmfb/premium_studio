const btSalvar = document.getElementById("bt-submit");

btSalvar.addEventListener("click", function(e){
    e.preventDefault();
    const title = document.getElementById('title').value;
    const deadline = document.getElementById('deadline').value;
    const description = document.getElementById('description').value;
    data = {
        "title": title,
        "deadline" : deadline,
        "description" : description
    }
    $.ajax({
        url : "/api/v1/task",
        type : 'post',
        data : JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        headers: {"Authorization": "Bearer " + getCookie('premium_access')}
   })
    .done(function(response, msg){
        console.log(response,msg);
        alert('Tarefa adicionada com sucesso!');
        window.location.replace("/exibir_projeto");
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



