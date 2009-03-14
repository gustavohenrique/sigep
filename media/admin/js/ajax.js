/**
 * Preenche um <select> de acordo com o item selecionado em outro <select>.
 * @component Componente que recebera o resultado
 * @id Item selecionado no <select> de origem
 * @url URL que tratara os dados
 */ 
function comboAjax(component, id, url) {
  // Cria uma variável dados em formato JSON, com 1 chave e 1 valor
  dados = {'id':id};
  urlsplit = url.split("/");
  fieldkey = urlsplit[urlsplit.length - 2];
  // É inserido um elemento option dentro do elemento select
  $("#"+component).html('<option value="0">Carregando...</option>');
  $.ajax({
    type: "POST",
    url: url,
    dataType: "json",
    data: dados,
    success: function(retorno){
      $("#"+component).empty();
      $.each(retorno, function(key, value) { 
        $("#"+component).append('<option value="'+value.pk+'">'+value.fields[fieldkey]+'</option>');
      });
    },
    error: function(erro) {
      alert('Erro: URL não encontrada.');
    }
  });
}