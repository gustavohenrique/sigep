/**
 * Ajusta a posicao e tamanho do menu, e etnão exibe-o na tela.
 * @component ID do elemento html que originou o evento.
 */ 
function showMenu(component,width, height, top, left) {
  var position, menu;
  // position contem o width, height, top e left do componente
  position = $('#'+component).offset();
  // O ID do menu deve ser o mesmo do componente, porem com sufixo _float
  menu = component+'_float'; 
  
  // esconde todos os menus
  $('.menufloat').hide(); 
  if (width > 0) $('#'+menu).css({ width: width });
  if (height > 0) $('#'+menu).css({ height: height });
  if (top > 0) $('#'+menu).css({ top: top }); else $('#'+menu).css({ top: position.top });
  if (left > 0) $('#'+menu).css({ left: left }); else $('#'+menu).css({ left: position.left });
  // exibe o menu na tela apos definida sua posicao e tamanho
  $('#'+menu).show(); 
  
  // quando o menu perder o foco, eh iniciado o evento para esconde-lo apos algum tempo
  $('#'+menu).mouseover(function() { menuIsVisible = true; });
  $('#'+menu).mouseout(function() { menuIsVisible = false; hideMenu(menu); });
}

/**
 * Esconde um menu apos um determinado periodo de tempo (1,5s).
 */ 
function hideMenu(menu) {
  // apos 1500 ms, esconde todos os menu se nao houver foco sobre nenhu,
  window.setTimeout(function() { if (! menuIsVisible) $('#'+menu).hide(); }, 1500);
}

/**
 * Submete o form que contem o datagrid.
 * @url URL que ira tratar o form
 * @confirmation Indica se deve exibir um pedido de confirmacao antes de submeter o form
 */ 
function submitForm(url, confirmation) {
  if (url == '')
    alert('Nao foi configurada uma ação para esse menu.');
  else {
    id = $('#grid_form input:radio:checked').val();
    if (! id > 0)
      alert('Erro: Nenhum item selecionado.');
    else {
      if (confirmation) {
        if (confirm('Tem certeza?')) {
          $('#grid_form').attr('action',url);
          $('#grid_form').submit();
        }
      } else {
        $('#grid_form').attr('action',url);
        $('#grid_form').submit();      
      }
    }
  }
  
}