$(document).ready(function(){
    console.log("Hi");
    $("#menu-toggle").click(function(e){
      console.log("Hi");
      e.preventDefault();
      $("#wrapper").toggleClass("menuDisplayed");
    });
  });
  