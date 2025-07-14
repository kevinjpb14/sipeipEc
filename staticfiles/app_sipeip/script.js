

function obtenerValor() {
    var hselectsect = document.getElementById("hselect-sect");
    var hselectsubsect = document.getElementById("hselect-subsect");
    var hselectnivelgobierno = document.getElementById("hselect-nivelgobierno");


    // Obtén el elemento select
    var selectElement1 = document.getElementById("select-sect");
    var selectElement2 = document.getElementById("select-subsect");
    var selectElement3 = document.getElementById("select-nivelgobierno");

    // Obtén el valor seleccionado
    var valorSeleccionado1 = selectElement1.options[selectElement1.selectedIndex];
    var valorSeleccionado2 = selectElement2.options[selectElement2.selectedIndex];
    var valorSeleccionado3 = selectElement3.options[selectElement3.selectedIndex];


    // Hacer algo con el valor seleccionado (por ejemplo, mostrarlo en la consola)
    hselectsect.value = valorSeleccionado1.value;
    hselectsubsect.value = valorSeleccionado2.value;
    hselectnivelgobierno.value = valorSeleccionado3.textContent;

}


