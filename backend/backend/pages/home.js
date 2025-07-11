   document.addEventListener('DOMContentLoaded', async () => {
  const token = localStorage.getItem('accessToken');

  if (!token) {
    alert('No access token found. Please log in.');
    return;
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/teaches/', {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      alert('Failed to fetch teaches: ' + (errorData.detail || response.statusText));
      return;
    }

    const teaches = await response.json();
    console.log('Teaches:', teaches);

    const grid = document.querySelector('.grid');
    grid.innerHTML = ''; // Clear existing content

    teaches.forEach(item => {
      const subject = item.subject;
      const department = subject.department?.name || 'Unknown';
      const card = document.createElement('a');
      card.className = 'bg-white rounded-lg shadow-md overflow-hidden hover:bg-gray-100';
      card.href = `http://127.0.0.1:5500/pages/Dashboard.html?subject=${encodeURIComponent(subject.name)}`;

      card.innerHTML = `
        <img class="w-full h-32 object-cover" src="https://storage.googleapis.com/a1aa/image/ETnJUFyWb3oNiIh2uBoDb40e4i_Hfnmn-WbHYQSDOYs.jpg" alt="Course image">
        <div class="p-4">
          <h2 class="text-lg font-semibold mb-2">${subject.name}</h2>
          <p class="text-gray-600 text-sm mb-2">
            communication | grade ${subject.grade}  | ${subject.code}  | credit hours ${subject.credit_hours}
          </p>
        </div>
      `;
      grid.appendChild(card);
    });

  } catch (error) {
    console.error('Fetch error:', error);
    alert('An error occurred while fetching teaches data.');
  }
});
