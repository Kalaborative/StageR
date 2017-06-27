$(document).ready(function(){
	$('#toggle').click(function(){
    	$('#target').toggleClass('active');
  });
	$(".chat_inner-item").click(function(){
      var myDiv = document.getElementById("currentSinger");
      myDiv.innerHTML += this.innerHTML
      $(this).fadeOut('fast');
    });
});