$(document).ready(function(){
	$('#toggle').click(function(){
    	$('#target').toggleClass('active');
  });
    $("#next").click(function(){
    	$("#currentSinger").css("color", "#00ff7f");
    	$("img").first().slideUp('fast');
    });
    $("#skip").click(function(){
    	$("#currentSinger").css("color", "#A9A9A9");
    	$("#currentSinger").css("text-decoration", "line-through");
    	$("img").first().slideUp('fast');
    })
});