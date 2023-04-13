typingAnimation();
function typingAnimation () {
	console.log("Running");
	let elements = document.getElementsByClassName("typingAnimation");
	for(let e of elements) {
		let text = e.innerHTML;
		e.innerHTML = ""; // make the text empty
		let arr = text.split("");
		let speed = Number(e.getAttribute('typingSpeed') ?? 60)
		let loop = ()=> {
			if (arr.length > 0) {
				e.innerHTML = e.innerHTML + arr.shift();
				setTimeout(loop, speed);
			}
		}
		loop();
	}
}
