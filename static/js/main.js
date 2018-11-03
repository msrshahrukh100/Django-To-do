$(function(){

$(".dropdown-trigger").dropdown();


$('.mark-done').on('click', function(){
	var url = $(this).data('href')
	console.log(url)
	$.ajax({
		type: 'GET',
		url: url,
		success: function(data){
			console.log(data['done'])
			if(data['done']){
				  M.toast({html: 'Marked as Completed'})
				  window.setTimeout(function(){location.reload()},1500)

			}
		}
	})
})



$('.mark-deleted').on('click', function(){
	var url = $(this).data('href')
	console.log(url)
	if(confirm("Are you sure you want to delete this?")){
		$.ajax({
			type: 'GET',
			url: url,
			success: function(data){
					  M.toast({html: 'Deleted the Task'})
					  window.setTimeout(function(){location.reload()},1500)
			}
		})
	}
})

$('#search').on('click', function(){
	var query = $('#searchby').val()
	$('#search-results').html("")
	// console.log("ss")

	if(query != ""){
		$.ajax({
		  url: $(this).data('href'),
		  type: "get",
		  data: { 
		    query: query
		  },
		  success: function(data) {
		    $.each(data, function(index, data){
		    	// console.log(data)
		    	$('#search-results').append("<li class='collection-item'>"+data['title']+"</li>")
		    })
		  },
		});
	}
})



})
