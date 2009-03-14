grid_url = '/client/ajax/datagridx/';
grid_fields = {
  'NOME': '300px',
  'TELEFONE': '100px',
  'CELULAR': '100px',
  'BAIRRO': '100px'
};
grid_custom_menu = {
  'Editar': {'url':'/client/edit/', 'confirmation':false, 'ajax':false},
  'Excluir':{'url':'#', 'ajax':'deleteAjax()'},
  'Pontos de Rede':{'url':'#', 'ajax':'networkNode()'},
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

function networkNode() {
  var id = $('#grid_form :input:radio:checked').val();
  if (id > 0)
    window.open('/networknode/list/?id='+id,'Ponto de Rede','width=760,height=400,scrollbars=1,status=0,location=0,resizable=0');
  else
    alert('Selecione um cliente.');
}

