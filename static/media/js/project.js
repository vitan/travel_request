$(function(){
	//datepicker
	$(function() {
	$( "#datepicker1,#datepicker2,#datepicker3" ).datepicker({dateFormat:"DD,d,MM,yy"});
	});
	//select the option(Others) show the input panel
	$("#select-location").change(function(){
		if($("#select-location option:selected").text()=='Others')
			$("#dialog-location").show();	 
	})
	$("#select-location2").change(function(){
		if($("#select-location2 option:selected").text()=='Others')
			$("#dialog-location2").show();	 
	})
	$("#add-location1").click(function(){		
			$("#dialog-location").show();	 
	})
	$("#add-location2").click(function(){		
			$("#dialog-location2").show();	 
	})
	//add the input text to select
	$("#location-btn").click(function(){	
			var value=$("#select-input").val();
   $("#select-location").append("<option selected="+"selected"+">"+value+"</option>");
	$("#dialog-location").hide(); 
	})
	$("#location-btn2").click(function(){	
			var value=$("#select-input2").val();
   $("#select-location2").append("<option selected="+"selected"+">"+value+"</option>");
	$("#dialog-location2").hide(); 
	})
})