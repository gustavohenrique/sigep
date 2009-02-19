/**
 * Esconde/Exibe uma janela.
 * Se a janela estiver visivel, entao a esconde e muda o icone do botao,
 * senão faz o contrario.
 * @button_id Botao que disparou o evento
 */ 
function hide_show_window(button_id) {
  if (button_id == 'windowlisting_hide_show')
    $('#windowlisting').toggleClass('windowhidden');
  else
    $('#windowform').toggleClass('windowhidden');
  
  $('#'+button_id).toggleClass('buttonshow');

}



