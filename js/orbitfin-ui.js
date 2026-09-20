/**
 * Helpers compartilhados de interface do OrbitFin.
 * Carregado antes do script inline de cada pagina interna.
 */
(function (global) {
    'use strict';

    /**
     * Nome de exibicao do usuario.
     * O backend devolve `name`; `first_name`/`last_name` ficam como
     * compatibilidade. Sem nenhum deles, usa a parte local do e-mail.
     */
    function displayName(user) {
        if (!user) return 'Usuário';
        var composto = [user.first_name, user.last_name].filter(Boolean).join(' ').trim();
        var nome = (user.name || '').trim() || composto;
        if (nome) return nome;
        if (user.email) return String(user.email).split('@')[0];
        return 'Usuário';
    }

    /** Iniciais para o avatar, no maximo duas letras. */
    function initials(nome) {
        var partes = String(nome || '').trim().split(/\s+/).filter(Boolean);
        if (!partes.length) return '—';
        var ini = partes[0][0] + (partes.length > 1 ? partes[partes.length - 1][0] : '');
        return ini.toUpperCase();
    }

    /** Preenche nome e avatar do sidebar a partir do usuario autenticado. */
    function fillUserIdentity(user) {
        var nome = displayName(user);
        var elNome = document.getElementById('sidebarName');
        var elAvatar = document.getElementById('sidebarAvatar');
        var elWelcome = document.getElementById('welcomeName');
        if (elNome) elNome.textContent = nome;
        if (elAvatar) elAvatar.textContent = initials(nome);
        if (elWelcome) elWelcome.textContent = nome.split(' ')[0] + '!';
        return nome;
    }

    /**
     * Mostra um aviso de falha no lugar do conteudo, com opcao de repetir.
     * Sem isto a tela fica silenciosamente vazia e parece "sem dados".
     */
    function showDataError(alvo, mensagem, aoRepetir) {
        var box = typeof alvo === 'string' ? document.querySelector(alvo) : alvo;
        if (!box) return;
        var ehLinhaDeTabela = box.tagName === 'TBODY';
        var colunas = ehLinhaDeTabela
            ? (box.closest('table') ? box.closest('table').querySelectorAll('th').length || 1 : 1)
            : 0;
        var conteudo =
            '<div class="data-error" role="alert">' +
                '<span class="data-error-msg">' + mensagem + '</span>' +
                (aoRepetir ? '<button type="button" class="data-error-retry">Tentar de novo</button>' : '') +
            '</div>';
        box.innerHTML = ehLinhaDeTabela
            ? '<tr><td colspan="' + colunas + '">' + conteudo + '</td></tr>'
            : conteudo;
        if (aoRepetir) {
            var btn = box.querySelector('.data-error-retry');
            if (btn) btn.addEventListener('click', function () { aoRepetir(); });
        }
    }

    /**
     * Busca o usuario autenticado e preenche a identidade do sidebar.
     * Falha em silencio no visual (mantem o placeholder) e devolve null.
     */
    function loadUserIdentity(baseUrl, token) {
        if (!token) return Promise.resolve(null);
        return fetch(baseUrl + '/api:FODf7XFO/auth/me', {
            headers: { Authorization: 'Bearer ' + token }
        })
            .then(function (r) { if (!r.ok) throw new Error('auth/me ' + r.status); return r.json(); })
            .then(function (user) { fillUserIdentity(user); return user; })
            .catch(function (e) { console.error('Nao foi possivel carregar o usuario:', e); return null; });
    }

    global.OrbitFinUI = {
        displayName: displayName,
        initials: initials,
        fillUserIdentity: fillUserIdentity,
        loadUserIdentity: loadUserIdentity,
        showDataError: showDataError
    };
})(window);
