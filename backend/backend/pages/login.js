document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');

  form.addEventListener('submit', async (event) => {
    event.preventDefault(); // prevent page refresh

    const email = document.getElementById('username').value; // treated as email
    const password = document.getElementById('password').value;

    try {
      const response = await fetch('http://localhost:8000/accounts/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        alert('Login failed: ' + (data.detail || data.message || 'Invalid credentials'));
        return;
      }

      //alert('Login successful!');
      //console.log('Tokens:', data);

      // Save JWT tokens if available
      if (data.access) {
        localStorage.setItem('accessToken', data.access);
        localStorage.setItem('refreshToken', data.refresh);
      }

      // Redirect to the home page
      location.replace("Home.html");


    } catch (error) {
      alert('Error: ' + error.message);
    }
  });
});
