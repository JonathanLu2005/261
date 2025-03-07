junctionCard.addEventListener("click", () => {
    const modal = new bootstrap.Modal(document.getElementById("junctionDetailsModal"));
    modal.show();

    document.getElementById("modalJunctionName").textContent = junction.junctionname;

    const modalImage = document.querySelector("#junctionDetailsModal img");
    modalImage.src = junction.imageUrl || "static/example.jpg"; 
});