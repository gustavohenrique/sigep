grid_url = '/client/ajax/datagridx/';
grid_fields = {
  'NOME': '300px',
  'TELEFONE': '100px',
  'CELULAR': '100px',
  'BAIRRO': '100px'
};
grid_custom_menu = {
  'Editar': {'url':'/client/edit/', 'confirmation':false, 'ajax':false},
  'Excluir':{'url':'#', 'ajax':'deleteAjax()'}
};

function deleteAjax() {
  if (confirm('Tem certeza?')) {
    var dados;
    dados = {'id':$('#grid_form :input:radio:checked').val()}
    $.ajax({
      type: 'POST',
      url: '/client/ajax/deletex/',
      dataType: "json",
      data: dados,
      success: function(retorno) {
        page = $('#id_current').text();
        _pagination(page, grid_url);
        //alert('ok, foi');
      },
      error: function(error) {
        alert('Erro: '+error);
      }
    });
  }
}

