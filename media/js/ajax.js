/**
 * Preenche um <select> a partir do item selecionado em outro <select>
 * @component <select> de destino, que recebera o resultado
 * @id ID usado para filtrar a consulta
 * @url URL que recebera a requisicao via ajax
 */ 
function comboAjax(component, id, url) {
  dados = {'id':id};
  $("#"+component).html('<option value="0">Carregando...</option>');
  $.ajax({
    type: "POST",
    url: url,
    dataType: "json",
    data: dados,
    success: function(retorno) {
      urlsplit = url.split('/');
      fieldkey = urlsplit[urlsplit.length-2];
      $("#"+component).empty();
      $.each(retorno, function(i, item) {
        $("#"+component).append('<option value="'+item.pk+'">'+item.fields[fieldkey]+'</option>');
      });
    },
    error: function(erro) {
      alert('Erro. Sem retorno da requisicao.');
    }
  });
}
