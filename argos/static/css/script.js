document.addEventListener("DOMContentLoaded", function() {
    const tocItems = document.querySelectorAll("#stages li a");
    const sections = document.querySelectorAll(".content article");

    window.addEventListener("scroll", () => {
        let current = "";

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - 60) {
                current = section.getAttribute("id");
            }
        });

        tocItems.forEach(item => {
            item.parentElement.classList.remove("active");
            if (item.getAttribute("href").substring(1) === current) {
                item.parentElement.classList.add("active");
            }
        });
    });
});