(() => {

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
