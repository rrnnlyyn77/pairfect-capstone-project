// SKIN TYPE CAROUSEL FUNCTIONALITY
const wrapper = document.querySelector('.skin-cards-wrapper');
const arrowLeft = document.querySelector('.arrow-left');
const arrowRight = document.querySelector('.arrow-right');
const dots = document.querySelectorAll('.carousel-dot');

let currentIndex = 0;

function updateDots() {
    dots.forEach((dot, index) => {
        dot.classList.toggle("active", index === currentIndex);
    });
}

if (wrapper && arrowLeft && arrowRight) {
    arrowLeft.addEventListener('click', () => {
        currentIndex = Math.max(currentIndex - 1, 0);
        wrapper.scrollBy({ left: -wrapper.clientWidth, behavior: 'smooth' });
        updateDots();
    });

    arrowRight.addEventListener('click', () => {
        currentIndex = Math.min(currentIndex + 1, dots.length - 1);
        wrapper.scrollBy({ left: wrapper.clientWidth, behavior: 'smooth' });
        updateDots();
    });

    dots.forEach((dot, index) => {
        dot.addEventListener("click", () => {
            currentIndex = index;
            wrapper.scrollTo({ 
                left: wrapper.clientWidth * index, 
                behavior: "smooth"
            });
            updateDots();
        });
    });
}

console.log("PAIRFECT frontend ready.");

// Ingredient compatibility matrix (Y/N)
const compatibility = {
    "Niacinamide": {
        mix: ["Hyaluronic Acid", "Ceramides", "SPF", "Azelaic Acid"],
        avoid: ["Vitamin C"]
    },
    "Salicylic Acid": {
        mix: ["Niacinamide", "Hyaluronic Acid", "Ceramides"],
        avoid: ["Retinol", "Glycolic Acid", "Lactic Acid", "Ascorbic Acid"]
    },
    "Hyaluronic Acid": {
        mix: ["Everything"],
        avoid: []
    },
    "Kojic Acid": {
        mix: ["Niacinamide", "Hyaluronic Acid", "Azelaic Acid"],
        avoid: ["Retinol", "Vitamin C"]
    },
    "Ascorbic Acid": {
        mix: ["Hyaluronic Acid", "SPF"],
        avoid: ["Niacinamide", "AHA", "BHA", "Retinol"]
    },
    "Retinol": {
        mix: ["Hyaluronic Acid", "Ceramides"],
        avoid: ["AHA", "BHA", "Vitamin C", "Kojic Acid"]
    },
    "Ceramides": {
        mix: ["Everything"],
        avoid: []
    },
    "SPF": {
        mix: ["Everything"],
        avoid: []
    },
    "Glycolic Acid": {
        mix: ["Hyaluronic Acid", "SPF"],
        avoid: ["Retinol", "Vitamin C", "Niacinamide"]
    },
    "Lactic Acid": {
        mix: ["Hyaluronic Acid"],
        avoid: ["Retinol", "Vitamin C", "Niacinamide"]
    },
    "Azelaic Acid": {
        mix: ["Niacinamide", "Hyaluronic Acid", "Kojic Acid"],
        avoid: ["Vitamin C"]
    }
};

// OPEN MODAL
function openIngredient(name, imgFile) {
    const modal = document.getElementById("ingredientModal");
    modal.style.display = "flex";

    document.getElementById("modalName").innerText = name;

    document.getElementById("modalImg").src = "/static/images/ingredients/" + imgFile;

    let data = compatibility[name];

    const mixList = document.getElementById("mixList");
    const avoidList = document.getElementById("avoidList");

    mixList.innerHTML = "";
    avoidList.innerHTML = "";

    data.mix.forEach(m => mixList.innerHTML += `<li>${m}</li>`);
    data.avoid.forEach(a => avoidList.innerHTML += `<li>${a}</li>`);
}

// CLOSE MODAL
function closeModal() {
    document.getElementById("ingredientModal").style.display = "none";
}

//Image Upload

function triggerInput() {
    document.getElementById("imageInput").click();
}

function previewImage(event) {
    const preview = document.getElementById("preview");
    preview.src = URL.createObjectURL(event.target.files[0]);
    preview.style.display = "block";
}
