grid_url = '/networknode/ajax/datagridx/';
edit_url = '/networknode/edit/';

grid_fields = {
  'IP': '100px',
  'MAC': '100px',
  'PLANO': '100px',
  'AP/SWITCH': '100px',
  'ROTA': '100px',
  'USA PROXY': '100px',
  'BLOQUEADO': '80px',
  'AMARRADO': '80px'
};
grid_custom_menu = {
  //'Editar': {'url':'/networknode/edit/', 'confirmation':false, 'ajax':false},
  //'Excluir':{'url':'#', 'ajax':'deleteAjax()'},
  'Capturar MAC':{'url':'#', 'ajax':'getMAC()'},
  '(Des)bloquear IP':{'url':'#', 'ajax':'unBlockAjax()'},
  '(Des)amarrar MAC':{'url':'#', 'ajax':'unBoundAjax()'},
  '(Des)ativar Proxy':{'url':'#', 'ajax':'useproxyAjax()'}
};

function deleteAjax() {
  if (confirm('Tem certeza?')) {
    var dados;
    dados = {'id':$('#grid_form :input:radio:checked').val()}
    $.ajax({
      type: 'POST',
      url: '/networknode/ajax/deletex/',
      dataType: "json",
      data: dados,
      success: function(retorno) {
        page = $('#id_current').text();
        _pagination(page, grid_url);
        alert('IP removido com sucesso.');
      },
      error: function(error) {
        alert('Erro: '+error);
      }
    });
  }
}

function unBlockAjax() {
  var dados;
  dados = {'id':$('#grid_form :input:radio:checked').val()}
  $.ajax({
    type: 'POST',
    url: '/networknode/ajax/unblock/',
    dataType: "json",
    data: dados,
    success: function(retorno) {
      page = $('#id_current').text();
      _pagination(page, grid_url);
    },
    error: function(error) {
      alert('Erro: '+error);
    }
  });
}

function unBoundAjax() {
  var dados;
  dados = {'id':$('#grid_form :input:radio:checked').val()}
  $.ajax({
    type: 'POST',
    url: '/networknode/ajax/unbound/',
    dataType: "json",
    data: dados,
    success: function(retorno) {
      page = $('#id_current').text();
      _pagination(page, grid_url);
    },
    error: function(error) {
      alert('Erro: '+error);
    }
  });
}

function useproxyAjax() {
  var dados;
  dados = {'id':$('#grid_form :input:radio:checked').val()}
  $.ajax({
    type: 'POST',
    url: '/networknode/ajax/useproxy/',
    dataType: "json",
    data: dados,
    success: function(retorno) {
      page = $('#id_current').text();
      _pagination(page, grid_url);
    },
    error: function(error) {
      alert('Erro: '+error);
    }
  });
}