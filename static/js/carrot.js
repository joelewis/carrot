function create_frag(htmlStr) {
    var frag = document.createDocumentFragment(),
        temp = document.createElement('div');
    temp.innerHTML = htmlStr;
    while (temp.firstChild) {
        frag.appendChild(temp.firstChild);
    }
    return frag;
}

function insert_stuff(num) {
	var s = ' ', fragment = create(s);
	document.body.insertBefore(fragment,document.body.childNodes[0]);
}