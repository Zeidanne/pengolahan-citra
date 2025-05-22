document.addEventListener("DOMContentLoaded", function () {
    const imageInput = document.getElementById("image");
    const previewContainer = document.getElementById("preview-container");
    const previewImage = document.getElementById("preview");
    const imageComparisonContainer = document.querySelector(".image-comparison");
    const currentImageInfo = document.querySelector(".current-image-info");

    if (imageInput) {
        imageInput.addEventListener("change", function (e) {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function (event) {
                    if (previewImage) {
                        previewImage.src = event.target.result;
                    }
                    if (previewContainer) {
                        previewContainer.style.display = "block";
                    }
                    if (imageComparisonContainer) {
                        imageComparisonContainer.style.display = "none";
                    }
                };
                reader.readAsDataURL(this.files[0]);
            } else {
                if (previewImage) {
                    previewImage.src = "#";
                }
                if (previewContainer) {
                    previewContainer.style.display = "none";
                }
            }
        });
    }

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
            seSizeInput.value = sePlaceholders[selected] || "";
        });

        if(seTypeSelect.value) {
            seTypeSelect.dispatchEvent(new Event("change"));
        }
    }
});