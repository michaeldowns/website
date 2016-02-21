function starsFormatter(value) {
    var stars = ""
    for(var i=0; i < value; i++){
	stars += "<i class='glyphicon glyphicon-star'></i>"
    }
    return stars
}

function linkFormatter(value, row, index) {
    return "<a href='/problems/"+(index+1)+"'>"+value+"</a>";
}

function threadFormatter(value, row, index) {
    if(value == "solved"){
	return "<a href='thread/"+(index+1)+"'><i class='glyphicon glyphicon-ok'></i></a>";
    }else{
	return "<i class='glyphicon glyphicon-remove'></i>";
    }

}
