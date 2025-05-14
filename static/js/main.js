const imageInput = document.getElementById("image");
if (imageInput) {
    imageInput.addEventListener("change", function (e) {
        const previewContainer = document.getElementById("preview-container");
        const comparison = document.querySelector(".image-comparison");

        if (previewContainer) previewContainer.style.display = "block";
        if (comparison) comparison.style.display = "none";

        const reader = new FileReader();
        reader.onload = function (e) {
            const preview = document.getElementById("preview");
            if (preview) preview.src = e.target.result;
        };
        reader.readAsDataURL(this.files[0]);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const seTypeSelect = document.getElementById("se_type");
    const seSizeLabel = document.getElementById("se_size_label");
    const seSizeInput = document.getElementById("se_size");

    if (seTypeSelect && seSizeLabel && seSizeInput) {
        const sePlaceholders = {
            disk: "5",
            diamond: "3",
            line: "[10, 45]",
            rectangle: "[5, 10]",
            square: "4",
            octagon: "3",
            sphere: "3"
        };

        const seLabelHints = {
            disk: "Ukuran Elemen (radius, contoh: 5)",
            diamond: "Ukuran Elemen (radius, contoh: 3)",
            line: "Ukuran Elemen ([panjang, sudut], contoh: [10, 45])",
            rectangle: "Ukuran Elemen ([tinggi, lebar], contoh: [5, 10])",
            square: "Ukuran Elemen (panjang sisi, contoh: 4)",
            octagon: "Ukuran Elemen (radius, contoh: 3)",
            sphere: "Ukuran Elemen (radius untuk 3D, contoh: 3)"
        };

        seTypeSelect.addEventListener("change", function () {
            const selected = seTypeSelect.value;
            seSizeLabel.innerText = seLabelHints[selected] || "Ukuran Elemen:";
            seSizeInput.placeholder = sePlaceholders[selected] || "5";
            seSizeInput.value = sePlaceholders[selected] || "5";
        });

        seTypeSelect.dispatchEvent(new Event("change"));
    }
});
