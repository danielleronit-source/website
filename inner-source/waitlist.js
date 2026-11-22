(() => {
  const form = document.querySelector('.abundance-waitlist');
  if (!form) return;
  const hebrew = document.documentElement.lang === 'he';
  const button = form.querySelector('button[type="submit"]');
  const status = form.querySelector('.waitlist-status');
  const label = button.textContent;
  let sending = false;
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (sending) return;
    form.querySelectorAll('[required]').forEach((field) => { field.value = field.value.trim(); });
    if (!form.reportValidity()) return;
    sending = true;
    button.disabled = true;
    form.setAttribute('aria-busy', 'true');
    button.textContent = hebrew ? 'שולחת…' : 'Sending…';
    status.textContent = '';
    try {
      const response = await fetch('https://formsubmit.co/ajax/danielleronit@gmail.com', {
        method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' }, signal: AbortSignal.timeout(25000),
      });
      const result = await response.json();
      if (!response.ok || ![true, 'true'].includes(result.success)) throw new Error('Submission not accepted');
      form.reset();
      status.textContent = hebrew
        ? 'תודה! קיבלתי את הבקשה שלך להצטרף לרשימת ההמתנה. אעדכן אותך באימייל כשיתפרסמו פרטי המחזור הבא.'
        : 'Thank you! I’ve received your waitlist request. I’ll email you when details of the next Inner Source program are announced.';
    } catch {
      status.textContent = hebrew
        ? 'לא הצלחנו לאשר שהבקשה נשלחה. הפרטים שלך נשמרו בטופס. אפשר לנסות שוב או לשלוח אימייל לכתובת danielleronit@gmail.com.'
        : 'We couldn’t confirm your request was sent. Your details are still here. Please try again, or email danielleronit@gmail.com.';
    } finally {
      sending = false;
      button.disabled = false;
      button.textContent = label;
      form.removeAttribute('aria-busy');
    }
  });
})();
