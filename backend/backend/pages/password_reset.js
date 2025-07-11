    document.addEventListener('DOMContentLoaded', () => {
      const loginLink = document.querySelector('a.text-teal-600');
      loginLink.addEventListener('click', (event) => {
        event.preventDefault();
        location.replace("login.html");
      });
    });