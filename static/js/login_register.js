let p_trocar = document.getElementById('p_trocar');
let login_register_title = document.getElementById('login_register_title');
let hide_area = document.getElementById('hide-area');
let hide_enviar_login = document.getElementById('hide-enviar-login');
let next = document.getElementById('next');

//Função pra trocar o texto
function trocar_texto(){
    let input  = document.getElementById('variableToTellWhatWeAreUsing');

    //Condição para transformar em login
    if(input.value === 'register'){
        input.value = 'login';
        hide_area.classList.add('d-none');
        login_register_title.textContent = 'Fazer login';
        p_trocar.textContent = 'Não possui conta? Crie uma';
        next.classList.add('d-none')
        hide_enviar_login.classList.remove('d-none');
    }

    //Condição para transformar em cadastro
    else{
        input.value = 'register';
        hide_area.classList.remove('d-none');
        login_register_title.textContent = 'Criar uma conta';
        p_trocar.textContent = 'Já tem uma conta? Faça login';
        hide_enviar_login.classList.add('d-none');
        next.classList.remove('d-none')
    }
}

let getForm1 = document.getElementById('step1');
let getForm2 = document.getElementById('step2');
let submitArea = document.getElementById('submit-area');

function step(currentStep, event){
    event.preventDefault();

    //Volta pro passo 1
    if(currentStep == 1){
        next.classList.remove('d-none');
        getForm2.classList.add('d-none');
        getForm1.classList.remove('d-none');
    }

    //Passo 2
    else{
        getForm2.classList.remove('d-none');
        next.classList.add('d-none');
        getForm1.classList.add('d-none');
    }
}