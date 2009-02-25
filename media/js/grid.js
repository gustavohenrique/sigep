/**
 * @private
 * Recebe um dicionario contendo dados para criar o datagrid.
 * @page Numero da pagina
 * @url URL que recebera a requisicao ajax
 */ 
function _pagination(page, url) {
  var dados, text_search;
  search_text = $('#search_field').val();
  dados = {'page':page, 'search_text':search_text}
  $.ajax({
    type: 'POST',
    url: url,
    dataType: "json",
    data: dados,
    success: function(retorno) {
      
      // Para cada item do dicionario retornado...
      $.each(retorno, function(i, item) {
        // Atualiza os dados da barra de navegacao
        $('#id_previous_page_number').val(item.previous_page_number);
        $('#id_next_page_number').val(item.next_page_number);
        $('#id_current').text(item.current_page);
        $('#id_num_pages').text(item.num_pages);
        $('#id_total_result').text('TOTAL: '+item.total_result);
        
        // Obtem a lista com dados da consulta
        listing = item.listing;
        
        // Atualiza as linhas do datagrid com os novos dados
        $('#listing > tbody').empty();
        for (i=0; i<listing.length; i++) {
          list = listing[i];
          if (i % 2) row = 'row2'; else row = 'row1';
          $('#listing > tbody').append('<tr class="'+row+'">');
          $('#listing tr:last').append('<td><input type="radio" id="grid_row_id" name="id" value="'+list[0]+'"></td>');
          for(x=1; x < list.length; x++)
            $('#listing tr:last').append('<td>'+list[x]+'</td>');
          $('#listing').append('</tr>');
        }
      });
    },
    error: function(error) {
      alert('Erro: '+error);
    }
  });
}

/**
 * Procedimentos executados ao carregar o datagrid.
 */ 
$(document).ready(function() {
  // Atualiza o cabecalho da tabela com o nome dos campos
  $('#listing > thead').empty();
  $('#listing > thead').append('<tr>');
  $('#listing tr:last').append('<th style="width:10px"></th>');
  $.each(grid_fields, function(key, item) {
    $('#listing tr:last').append('<th style="width:'+item+'">'+key+'</th>');
  });
  $('#listing').append('</tr>');
  
  // Adiciona as acoes aos botoes de navegacao
  $('#firstbutton').click(function() {
    _pagination(1, grid_url);
  });
  $('#previousbutton').click(function() {
    page = $('#id_previous_page_number').val();
    _pagination(page, grid_url);
  });
  $('#nextbutton').click(function() {
    page = $('#id_next_page_number').val();
    _pagination(page, grid_url);
  });
  $('#lastbutton').click(function() {
    page = $('#id_num_pages').text();
    _pagination(page, grid_url);
  });
  
  // Ao ser carregado, preenche o datagrid com resultados da primeira pagina
  _pagination(1, grid_url);
  
  // Cria um menu flutuante de acordo com o array definido no modulo
  $.each(grid_custom_menu, function(key, value) {
    if (! value.ajax)
      $('#button_menu_float ul:last').append('<li><a href="#" onclick="submitForm(\''+value.url+'\','+value.confirmation+')">'+key+'</a></li>');
    else
      $('#button_menu_float ul:last').append('<li><a href="#" onclick="'+value.ajax+'">'+key+'</a></li>');
  });
  
  // Ajusta a posicao do menu flutuante e adiciona ao evento click do botao
  $('#button_menu').click(function() {
    var h, p;
    h = $('#'+this.id).height();
    p = $('#'+this.id).offset();
    top = (p.top - $('#button_menu_float').height());
    showMenu(this.id, 0, 0, top, p.left);
  });
  
  // Limpa o campo de busca ao obter foco
  $('#search_field').focus(function() { $(this).val(''); });
  // A cada tecla pressionada, atualiza o datagrid
  $('#search_field').keyup(function(event) { _pagination(1, grid_url); });
});



/**
 * Necessario descomentar ao usar em outro projeto.
 *

function showMenu(component,width, height, top, left) {
  var position, menu;
  position = $('#'+component).offset();
  menu = component+'_float'; // mesmo nome do componente, com sufixo _float
    
  $('.menufloat').hide(); // esconde todos os menus com class="menufloat"
  if (width > 0) $('#'+menu).css({ width: width });
  if (height > 0) $('#'+menu).css({ height: height });
  if (top > 0) $('#'+menu).css({ top: top }); else $('#'+menu).css({ top: position.top });
  if (left > 0) $('#'+menu).css({ left: left }); else $('#'+menu).css({ left: position.left });
  $('#'+menu).show(); // exibe o menu na tela apos definida sua posicao e tamanho
  
  // quando o menu perder o foco, eh iniciada a funcao que o esconde
  $('#'+menu).mouseover(function() { menuIsVisible = true; });
  $('#'+menu).mouseout(function() { menuIsVisible = false; hideMenu(menu); });
}

function hideMenu(menu) {
  // apos 1500 ms, esconde todos os menu se nao houver foco sobre nenhu,
  window.setTimeout(function() { if (! menuIsVisible) $('#'+menu).hide(); }, 1500);
}

 *
 */
