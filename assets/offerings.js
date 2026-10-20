(() => {

    document.querySelectorAll(".healing-quote-carousel").forEach((carousel) => {
      const track = carousel.querySelector(".quote-slides");
      const slides = Array.from(track.children);
      const position = carousel.querySelector(".quote-position");
      const current = () => Math.round(track.scrollLeft / track.clientWidth);
      const move = (direction) => {
        const next = (current() + direction + slides.length) % slides.length;
        track.scrollTo({left: next * track.clientWidth, behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth"});
      };
      carousel.querySelector("[data-quote-prev]").addEventListener("click", () => move(-1));
      carousel.querySelector("[data-quote-next]").addEventListener("click", () => move(1));
      track.addEventListener("keydown", (event) => {
        if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
        event.preventDefault();
        move(event.key === "ArrowRight" ? 1 : -1);
      });
      track.addEventListener("scroll", () => {
        position.textContent = `${current() + 1} of ${slides.length}`;
      }, {passive: true});
    });

    const faqItems = Array.from(document.querySelectorAll(".faq-item"));

    faqItems.forEach((item) => {
      item.addEventListener("toggle", () => {
        if (!item.open) return;

        faqItems.forEach((otherItem) => {
          if (otherItem !== item) {
            otherItem.open = false;
          }
        });
      });
    });

})();
