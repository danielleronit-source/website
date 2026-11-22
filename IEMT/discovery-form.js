(() => {
  document.querySelectorAll('.discovery-form').forEach((form) => {
    const button = form.querySelector('button[type="submit"]');
    const status = form.querySelector('.discovery-form-status');
    const hebrew = document.documentElement.lang === 'he';
    const buttonLabel = button.textContent;
    let submitting = false;

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (submitting) return;

      for (const field of form.querySelectorAll('[required]')) {
        field.value = field.value.trim();
      }
      if (!form.reportValidity()) return;

      submitting = true;
      button.disabled = true;
      form.setAttribute('aria-busy', 'true');
      button.textContent = hebrew ? 'שולחת…' : 'Sending…';
      status.textContent = '';

      try {
        const response = await fetch(
          'https://formsubmit.co/ajax/danielleronit@gmail.com',
          {
            method: 'POST',
            body: new FormData(form),
            headers: { Accept: 'application/json' },
            signal: AbortSignal.timeout(25000),
          },
        );
        const result = await response.json();
        if (!response.ok || ![true, 'true'].includes(result.success)) {
          throw new Error('Submission was not accepted');
        }
        form.reset();
        status.textContent = form.hasAttribute('data-question-form')
          ? (hebrew ? 'תודה על ההודעה. אחזור אליך באימייל.' : 'Thank you for your message. I’ll get back to you by email.')
          : hebrew
          ? 'תודה שפנית. אצור איתך קשר באימייל כדי לתאם את השיחה שלנו.'
          : 'Thank you for reaching out. I’ll email you to arrange our call.';
      } catch {
        status.textContent = hebrew
          ? 'לא הצלחנו לאשר שההודעה נשלחה. הפרטים שלך נשמרו בטופס. אפשר לנסות שוב או לשלוח אימייל לכתובת danielleronit@gmail.com.'
          : 'We couldn’t confirm your message was sent. Your details are still here. Please try again, or email me at danielleronit@gmail.com.';
      } finally {
        submitting = false;
        button.disabled = false;
        button.textContent = buttonLabel;
        form.removeAttribute('aria-busy');
      }
    });
  });

  const dialog = document.querySelector('#question-dialog');
  if (!dialog) return;
  document.querySelectorAll('[data-question-open]').forEach((opener) => {
    opener.addEventListener('click', (event) => {
      event.preventDefault();
      dialog.showModal();
    });
  });
  dialog.querySelector('.question-close').addEventListener('click', () => dialog.close());
})();
