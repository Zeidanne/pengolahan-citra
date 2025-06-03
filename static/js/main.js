document.addEventListener("DOMContentLoaded", function () {
    const imageInput     = document.getElementById("image");
    const previewContainer = document.getElementById("preview-container");
    const previewImage   = document.getElementById("preview");
    const imageComparisonContainer = document.querySelector(".image-comparison");
    const currentImageInfo = document.querySelector(".current-image-info");

    // Preview Gambar sebelum diproses
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

    // Bagian struktur elemen
    const methodSelect   = document.getElementById("method_morfologi");
    const seOptionsDiv   = document.getElementById("se_options");
    const seTypeSelect   = document.getElementById("se_type");
    const seSizeLabel    = document.getElementById("se_size_label");
    const seSizeInput    = document.getElementById("se_size");

    const methodsWithSE = [
        "opening",
        "closing",
        "boundary"
    ];

    const sePlaceholders = {
        disk:      "5",
        diamond:   "3",
        line:      "[10, 45]",
        rectangle: "[5, 10]",
        square:    "4",
        octagon:   "3",
        sphere:    "3"
    };

    const seLabelHints = {
        disk:      "Ukuran Elemen (radius, contoh: 5)",
        diamond:   "Ukuran Elemen (radius, contoh: 3)",
        line:      "Ukuran Elemen ([panjang, sudut], contoh: [10, 45])",
        rectangle: "Ukuran Elemen ([tinggi, lebar], contoh: [5, 10])",
        square:    "Ukuran Elemen (panjang sisi, contoh: 4)",
        octagon:   "Ukuran Elemen (radius, contoh: 3)",
        sphere:    "Ukuran Elemen (radius, contoh: 3)"
    };

    function toggleSeOptions() {
        const selectedMethod = methodSelect.value;
        if (methodsWithSE.includes(selectedMethod)) {
            seOptionsDiv.style.display = "block";
            seTypeSelect.setAttribute("required", "required");
            seSizeInput.setAttribute("required", "required");
        } else {
            seOptionsDiv.style.display = "none";
            seTypeSelect.removeAttribute("required");
            seSizeInput.removeAttribute("required");
        }
    }

    if (methodSelect && seOptionsDiv) {
        methodSelect.addEventListener("change", function () {
            toggleSeOptions();
        });
        if (methodSelect.value) {
            toggleSeOptions();
        }
    }

    if (seTypeSelect && seSizeLabel && seSizeInput) {
        seTypeSelect.addEventListener("change", function () {
            const sel = seTypeSelect.value;
            seSizeLabel.innerText = seLabelHints[sel] || "Ukuran Elemen:";
            seSizeInput.placeholder = sePlaceholders[sel] || "5";
            seSizeInput.value = sePlaceholders[sel] || "";
        });
        if (seTypeSelect.value) {
            seTypeSelect.dispatchEvent(new Event("change"));
        }
    }
});