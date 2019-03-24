$(function(){
	var myTextarea = $(".Codearea")[0];
	var editor = CodeMirror.fromTextArea(myTextarea, {
		lineNumbers: true,
		mode:"text/x-c++src",
		indentUnit: 4,
		theme:"base16-dark",
		indentWithTabs: true,
	});
	editor.setSize("100%" , "100%");
	$(".up-btn").click(function(){
	});
	var code_slects = $(".dropdown-menu>li>a");
	$(".re_Input").click(function(){
		editor.setValue("");
	});
	for(var i = 0;i < code_slects.length;i++){
	$(code_slects[i]).click(function(){
			editor.setOption("mode" , "text/x-" + $(this).attr('id'));
			$(".dropdown-toggle .slect-title").text($(this).text());
		});
	}
	var oVwidt = document.documentElement.clientWidth;
	var oCodeE = $(".Code-editing");
	var oProblem = $(".Problem-description");
	if(oVwidt <= 518){
		oCodeE.hide();
		oProblem.css({
			"margin":"auto",
			"margin-top":"1em",
			"margin-bottom":"3em",
			"width":"92vw",
		});
		editor.setSize("0%" , "0%");
	}
	function oVwidthChang(){
		var oVwidth = document.documentElement.clientWidth;
		console.log(oVwidth);
		if(oVwidth <= 518){
			oCodeE.hide();
			oProblem.css({
				"margin":"auto",
				"margin-top":"1em",
			"margin-bottom":"3em",
				"width":"92vw",
			});
			editor.setSize("0%" , "0%");
		}
		else{
			oCodeE.show();
			oProblem.css("margin" , "1em 0 1em 3em");
			oProblem.css("width" , "50%");
			editor.setSize("100%" , "100%");
		}
	}
	$(window).resize(function(){
		oVwidthChang();
	});
});