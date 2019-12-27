var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
var outputTotal = document.getElementById("demoTotal");
var weeklyNet = {{ weekly_net }}
output.innerHTML = slider.value;
outputTotal.innerText = (slider.value * weeklyNet * 0.01).toFixed(2);

slider.oninput = function() {
outputTotal.innerHTML = (this.value * weeklyNet * 0.01).toFixed(2);
output.innerHTML = this.value;

}
