(function () {

    const btnEliminacion=document.querySelectorAll(".btnEliminacion");

    btnEliminacion.forEach(btn=>{
        btn.addEventListener("click",(e)=>{
            const confirmacion=confirm("¿Seguro de eliminar a la persona?");
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });

})();