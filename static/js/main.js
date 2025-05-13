document.getElementById("image").addEventListener("change", function(e) {
    const previewContainer = document.getElementById("preview-container");
    const comparison = document.querySelector(".image-comparison");
    
    previewContainer.style.display = "block";
    comparison.style.display = "none";
    
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById("preview").src = e.target.result;
    }
    reader.readAsDataURL(this.files[0]);
});