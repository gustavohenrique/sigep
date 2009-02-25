grid_url = '/networknode/ajax/datagridx/';
grid_fields = {
  'IP': '100px',
  'MAC': '100px',
  'PLANO': '100px',
  'BLOQUEADO': '100px',
  'SEM MAC': '100px'
};
grid_custom_menu = {
  'Editar': {'url':'/client/edit/', 'confirmation':false, 'ajax':false},
  'Excluir':{'url':'#', 'ajax':'deleteAjax()'},
  'Bloquear':{'url':'#', 'ajax':'networkNode()'},
  'Liberar sem MAC':{'url':'#', 'ajax':'networkNode()'},
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



