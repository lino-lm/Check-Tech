// ========================================
// LOGIN DO ALUNO
// ========================================

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const email =
            document.getElementById("email").value.trim();

        const senha =
            document.getElementById("senha").value;

        const serie =
            document.getElementById("serie").value;

        try {

            const resposta = await fetch("/api/login", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    email: email,
                    senha: senha,
                    serie: serie
                })
            });

            const dados = await resposta.json();

            if (dados.sucesso) {

                alert("Login realizado com sucesso!");

                window.location.href = "/computador";

            } else {

                alert(
                    dados.mensagem ||
                    "E-mail, senha ou série incorretos."
                );

            }

        } catch (erro) {

            console.error("Erro no login:", erro);

            alert(
                "Não foi possível conectar ao servidor."
            );

        }

    });

}



// ========================================
// CADASTRO
// ========================================

const cadastroForm =
    document.getElementById("cadastroForm");

if (cadastroForm) {

    cadastroForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const nome =
            document.getElementById("nome").value.trim();

        const email =
            document.getElementById("emailCadastro")
                .value.trim();

        const senha =
            document.getElementById("senhaCadastro")
                .value;

        const serie =
            document.getElementById("serieCadastro")
                .value;

        try {

            const resposta = await fetch("/api/cadastro", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    nome: nome,
                    email: email,
                    senha: senha,
                    serie: serie
                })
            });

            const dados = await resposta.json();

            if (dados.sucesso) {

                alert("Conta criada com sucesso!");

                window.location.href = "/";

            } else {

                alert(
                    dados.mensagem ||
                    "Não foi possível criar a conta."
                );

            }

        } catch (erro) {

            console.error("Erro no cadastro:", erro);

            alert(
                "Não foi possível conectar ao servidor."
            );

        }

    });

}



// ========================================
// NAVEGAÇÃO
// ========================================

function irParaCadastro() {

    window.location.href = "/cadastro";

}


function voltarLogin() {

    window.location.href = "/";

}


function souProfessor() {

    window.location.href = "/login-professor";

}
// ========================================
// CADASTRO DO PROFESSOR
// ========================================

const professorCadastroForm =
    document.getElementById("professorCadastroForm");

if (professorCadastroForm) {

    professorCadastroForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const nome =
                document.getElementById(
                    "professorNome"
                ).value.trim();

            const email =
                document.getElementById(
                    "professorCadastroEmail"
                ).value.trim();

            const senha =
                document.getElementById(
                    "professorCadastroSenha"
                ).value;

            const codigo =
                document.getElementById(
                    "professorCodigo"
                ).value.trim();


            try {

                const resposta =
                    await fetch(
                        "/api/cadastro-professor",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                nome: nome,
                                email: email,
                                senha: senha,
                                codigo: codigo
                            })
                        }
                    );


                const dados =
                    await resposta.json();


                if (dados.sucesso) {

                    alert(
                        "Conta de professor criada com sucesso!"
                    );

                    window.location.href =
                        "/login-professor";

                } else {

                    alert(
                        dados.mensagem ||
                        "Não foi possível criar a conta."
                    );

                }

            } catch (erro) {

                console.error(
                    "Erro no cadastro do professor:",
                    erro
                );

                alert(
                    "Não foi possível conectar ao servidor."
                );

            }

        }
    );

}


function irParaCadastroProfessor() {

    window.location.href =
        "/cadastro-professor";

}


function voltarLoginProfessor() {

    window.location.href =
        "/login-professor";

}


// ========================================
// COMPUTADOR
// ========================================

const selectComputador =
    document.getElementById("computador");


if (selectComputador) {

    async function carregarComputadores() {

        try {

            const resposta =
                await fetch("/api/computadores");

            const dados =
                await resposta.json();

            if (!dados.sucesso) {

                alert(
                    dados.mensagem ||
                    "Não foi possível carregar os computadores."
                );

                return;

            }

            selectComputador.innerHTML = "";

            const opcaoInicial =
                document.createElement("option");

            opcaoInicial.value = "";

            opcaoInicial.textContent =
                "Selecione um computador";

            opcaoInicial.disabled = true;
            opcaoInicial.selected = true;

            selectComputador.appendChild(
                opcaoInicial
            );


            dados.computadores.forEach(
                function(computador) {

                    const opcao =
                        document.createElement("option");

                    opcao.value = computador;

                    opcao.textContent = computador;

                    selectComputador.appendChild(
                        opcao
                    );

                }
            );

        } catch (erro) {

            console.error(
                "Erro ao carregar computadores:",
                erro
            );

            alert(
                "Não foi possível carregar os computadores."
            );

        }

    }

    carregarComputadores();

}


function continuarComputador() {

    const computador =
        document.getElementById("computador").value;

    if (!computador) {

        alert("Selecione um computador.");

        return;

    }

    localStorage.setItem(
        "computador",
        computador
    );

    window.location.href = "/checklist";

}



// ========================================
// MOSTRAR COMPUTADOR NO CHECKLIST
// ========================================

const pcSelecionado =
    document.getElementById("pcSelecionado");


if (pcSelecionado) {

    const computador =
        localStorage.getItem("computador");

    if (computador) {

        pcSelecionado.textContent =
            computador;

    }

}



// ========================================
// CHECKLIST
// ========================================

const checklistForm =
    document.getElementById("checklistForm");


if (checklistForm) {

    checklistForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const computador =
                localStorage.getItem("computador");


            if (!computador) {

                alert(
                    "Nenhum computador foi selecionado."
                );

                window.location.href =
                    "/computador";

                return;

            }


            const notebookSelecionado =
                document.querySelector(
                    'input[name="notebook"]:checked'
                );

            const mouseSelecionado =
                document.querySelector(
                    'input[name="mouse"]:checked'
                );

            const bateriaSelecionada =
                document.querySelector(
                    'input[name="bateria"]:checked'
                );

            const carregadorSelecionado =
                document.querySelector(
                    'input[name="carregador"]:checked'
                );

            const mouseCarregadoSelecionado =
                document.querySelector(
                    'input[name="mouse_carregado"]:checked'
                );


            if (
                !notebookSelecionado ||
                !mouseSelecionado ||
                !bateriaSelecionada ||
                !carregadorSelecionado ||
                !mouseCarregadoSelecionado
            ) {

                alert(
                    "Responda todos os itens do checklist."
                );

                return;

            }


            const notebook =
                notebookSelecionado.value === "true";

            const mouse =
                mouseSelecionado.value === "true";

            const bateria =
                bateriaSelecionada.value === "true";

            const carregador =
                carregadorSelecionado.value === "true";

            const mouseCarregado =
                mouseCarregadoSelecionado.value === "true";


            const observacoes =
                document.getElementById("observacoes")
                    .value.trim();


            try {

                const resposta =
                    await fetch("/api/checklist", {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            computador: computador,

                            notebook: notebook,

                            mouse: mouse,

                            bateria: bateria,

                            carregador: carregador,

                            mouse_carregado:
                                mouseCarregado,

                            observacoes:
                                observacoes

                        })

                    });


                const dados =
                    await resposta.json();


                if (dados.sucesso) {

                    window.location.href =
                        "/sucesso";

                } else {

                    alert(
                        dados.mensagem ||
                        "Erro ao enviar checklist."
                    );

                }

            } catch (erro) {

                console.error(
                    "Erro no checklist:",
                    erro
                );

                alert(
                    "Não foi possível enviar o checklist."
                );

            }

        }
    );

}



// ========================================
// VOLTAR AO INÍCIO
// ========================================

function voltarInicio() {

    localStorage.removeItem("computador");

    window.location.href = "/";

}



// ========================================
// LOGIN DO PROFESSOR
// ========================================

const professorLoginForm =
    document.getElementById("professorLoginForm");


if (professorLoginForm) {

    professorLoginForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const email =
                document.getElementById(
                    "professorEmail"
                ).value.trim();


            const senha =
                document.getElementById(
                    "professorSenha"
                ).value;


            try {

                const resposta =
                    await fetch(
                        "/api/login-professor",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                email: email,
                                senha: senha
                            })
                        }
                    );


                const dados =
                    await resposta.json();


                if (dados.sucesso) {

                    window.location.href =
                        "/professor";

                } else {

                    alert(
                        dados.mensagem ||
                        "Não foi possível entrar."
                    );

                }

            } catch (erro) {

                console.error(
                    "Erro no login do professor:",
                    erro
                );

                alert(
                    "Não foi possível conectar ao servidor."
                );

            }

        }
    );

}



// ========================================
// HUB DO PROFESSOR
// ========================================

const professorBody =
    document.querySelector(".professor-body");


if (professorBody) {

    carregarDashboardProfessor();

}


async function carregarDashboardProfessor() {

    try {

        const resposta =
            await fetch(
                "/api/professor/dashboard"
            );


        if (resposta.status === 403) {

            window.location.href =
                "/login-professor";

            return;

        }


        const dados =
            await resposta.json();


        if (!dados.sucesso) {

            alert(
                dados.mensagem ||
                "Não foi possível carregar o Hub."
            );

            return;

        }


        // ====================================
        // PROFESSOR
        // ====================================

        if (dados.professor) {

            const nome =
                dados.professor.nome ||
                "Professor";


            document.getElementById(
                "teacherName"
            ).textContent = nome;


           document.getElementById(
                "teacherEmail"
           ).textContent =
                dados.professor.email || "Professor";


            const iniciais =
                nome
                    .split(" ")
                    .filter(Boolean)
                    .slice(0, 2)
                    .map(
                        parte =>
                            parte
                                .charAt(0)
                                .toUpperCase()
                    )
                    .join("");


            document.getElementById(
                "teacherAvatar"
            ).textContent =
                iniciais || "P";

        }


        // ====================================
        // ESTATÍSTICAS
        // ====================================

        document.getElementById(
            "totalPcs"
        ).textContent =
            dados.total_pcs ?? 0;


        document.getElementById(
            "problemasPcs"
        ).textContent =
            dados.problemas_pcs ?? 0;


        document.getElementById(
            "ultimaChecagem"
        ).textContent =
            formatarTempo(
                dados.ultima_checagem
            );


        // ====================================
        // PAINÉIS
        // ====================================

        renderizarProblemas(
            dados.problemas || []
        );


        renderizarComentarios(
            dados.comentarios || []
        );


        renderizarVerificacoes(
            dados.ultimas_verificacoes || []
        );


    } catch (erro) {

        console.error(
            "Erro ao carregar dashboard:",
            erro
        );

        alert(
            "Não foi possível carregar os dados do Hub."
        );

    }

}



// ========================================
// PROBLEMAS
// ========================================

function renderizarProblemas(problemas) {

    const container =
        document.getElementById(
            "problemasContainer"
        );


    if (!container) {
        return;
    }


    container.innerHTML = "";


    if (!problemas.length) {

        container.innerHTML = `
            <div class="panel-empty">
                Nenhum problema encontrado.
            </div>
        `;

        return;

    }


    problemas.forEach(
        function(registro) {

            const listaProblemas =
                registro.problemas || [];


            listaProblemas.forEach(
                function(problema) {

                    const item =
                        document.createElement(
                            "div"
                        );


                    item.className =
                        "problem-item";


                    item.innerHTML = `

                        <span class="problem-pc">
                            ${escapeHtml(
                                registro.computador ||
                                "--"
                            )}
                        </span>

                        <span class="problem-description">
                            ${escapeHtml(
                                problema
                            )}
                        </span>

                    `;


                    container.appendChild(item);

                }
            );

        }
    );


    if (!container.children.length) {

        container.innerHTML = `
            <div class="panel-empty">
                Nenhum problema encontrado.
            </div>
        `;

    }

}



// ========================================
// COMENTÁRIOS
// ========================================

function renderizarComentarios(comentarios) {

    const container =
        document.getElementById(
            "comentariosContainer"
        );


    if (!container) {
        return;
    }


    container.innerHTML = "";


    if (!comentarios.length) {

        container.innerHTML = `
            <div class="panel-empty">
                Nenhum comentário registrado.
            </div>
        `;

        return;

    }


    comentarios.forEach(
        function(comentario) {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "comment-item";


            item.innerHTML = `

                <div class="comment-header">

                    ${escapeHtml(
                        comentario.computador ||
                        "--"
                    )}

                    /

                    ${escapeHtml(
                        comentario.aluno ||
                        "Aluno"
                    )}

                </div>


                <div class="comment-text">

                    ${escapeHtml(
                        comentario.observacoes ||
                        ""
                    )}

                </div>

            `;


            container.appendChild(item);

        }
    );

}



// ========================================
// ÚLTIMAS VERIFICAÇÕES
// ========================================

function renderizarVerificacoes(verificacoes) {

    const container =
        document.getElementById(
            "verificacoesContainer"
        );


    if (!container) {
        return;
    }


    container.innerHTML = "";


    if (!verificacoes.length) {

        container.innerHTML = `
            <div class="panel-empty">
                Nenhuma verificação registrada.
            </div>
        `;

        return;

    }


    verificacoes.forEach(
        function(verificacao) {

            const item =
                document.createElement(
                    "div"
                );


            const temProblema =
                verificacao.problemas &&
                verificacao.problemas.length > 0;


            item.className =
                temProblema
                    ? "verification-item has-problem"
                    : "verification-item";


            let textoStatus = "OK";


            if (temProblema) {

                textoStatus =
                    "Problema: " +
                    verificacao.problemas.join(
                        ", "
                    );

            }


            item.innerHTML = `

                <div class="verification-pc">

                    ${escapeHtml(
                        verificacao.computador ||
                        "--"
                    )}

                    /

                </div>


                <div class="verification-status">

                    ${escapeHtml(
                        textoStatus
                    )}

                </div>

            `;


            container.appendChild(item);

        }
    );

}



// ========================================
// FORMATAR TEMPO
// ========================================

function formatarTempo(dataString) {

    if (!dataString) {

        return "--";

    }


    const data =
        new Date(dataString);


    if (Number.isNaN(data.getTime())) {

        return "--";

    }


    const agora =
        new Date();


    const diferenca =
        Math.floor(
            (agora - data) / 1000
        );


    if (diferenca < 60) {

        return "Agora";

    }


    const minutos =
        Math.floor(
            diferenca / 60
        );


    if (minutos < 60) {

        return minutos === 1
            ? "1 min atrás"
            : `${minutos} mins atrás`;

    }


    const horas =
        Math.floor(
            minutos / 60
        );


    if (horas < 24) {

        return horas === 1
            ? "1 hora atrás"
            : `${horas} horas atrás`;

    }


    const dias =
        Math.floor(
            horas / 24
        );


    return dias === 1
        ? "1 dia atrás"
        : `${dias} dias atrás`;

}



// ========================================
// PROTEÇÃO CONTRA HTML INJETADO
// ========================================

function escapeHtml(valor) {

    const div =
        document.createElement("div");


    div.textContent =
        valor ?? "";


    return div.innerHTML;

}



// ========================================
// LOGOUT DO PROFESSOR
// ========================================

async function logoutProfessor() {

    try {

        await fetch(
            "/api/logout",
            {
                method: "POST"
            }
        );

    } catch (erro) {

        console.error(
            "Erro ao sair:",
            erro
        );

    }


    window.location.href = "/";

}