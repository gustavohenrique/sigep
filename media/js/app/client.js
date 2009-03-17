grid_url = '/client/ajax/datagridx/';
edit_url = '/client/edit/';
grid_fields = {
  'NOME': '300px',
  'TELEFONE': '100px',
  'CELULAR': '100px',
  'BAIRRO': '100px'
};
grid_custom_menu = {
  'Contrato':{'url':'#', 'ajax':'agreement()'},
  'Cancelamento da Conta':{'url':'#', 'ajax':'cancelAccount()'},
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

