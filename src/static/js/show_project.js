// Adicionar nova tarefa:
const btNewTask = document.getElementById("bt-new-task");
btNewTask.addEventListener("click", function(e) {
    e.preventDefault();
    window.location.replace("/tarefa")
});

// Ocultar concluidas:
const btOcultarConcluidas = document.getElementById("flexSwitchOcultarConcluidas");
btOcultarConcluidas.addEventListener("click", function(){
    if (btOcultarConcluidas.checked == true) {
        alert("Ocultou as tarefas concluidas");
    } else {
        alert("Mostrou as tarefas concluidas");
    }
});

// Deletar tarefas:
document.querySelectorAll("#bt-delete-task").forEach(item => {
    item.addEventListener("click", () => {
        let nomeTarefa = item.parentElement.querySelector("#taskName").textContent;
        alert(`Clicou para deletar a tarefa: ${nomeTarefa}`);
    })
});

// Marcar tarefa como concluida:
document.querySelectorAll("#flexCheckDefault").forEach(item =>{
    item.addEventListener("click", () =>{
        let nomeTarefa = item.parentElement.querySelector("#taskName").textContent;
        if (item.checked == true){
            alert(`Concluiu a tarefa: ${nomeTarefa}`);
        } else {
            alert(`Restaurou a tarefa: ${nomeTarefa}`);
        }
    })
});
