document.addEventListener('DOMContentLoaded', async () => {
  const token = localStorage.getItem('accessToken');
  const tbody = document.querySelector('tbody');

  if (!token) {
    alert('No access token found. Please log in.');
    return;
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/requests/', {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      alert('Failed to fetch requests: ' + (errorData.detail || response.statusText));
      return;
    }

    const requests = await response.json();
    tbody.innerHTML = '';

    requests.forEach(req => {
      const tr = document.createElement('tr');
      tr.className = 'bg-yellow-100';

      const statusColor =
        req.status === 'approved'
          ? 'bg-green-500'
          : req.status === 'rejected'
          ? 'bg-red-500'
          : 'bg-yellow-500';

      tr.innerHTML = `
        <td class="p-3">${new Date(req.created_at).toLocaleDateString()}</td>
        <td class="p-3">${req.student.account.name} (${req.student.student_code})</td>
        <td class="p-3">Subject ${req.subject.name} (${req.subject.code})</td>
        <td class="p-3">${req.description}</td>
        <td class="p-3">${req.request_type}</td>
        <td class="p-3"><span class="${statusColor} text-white px-2 py-1 rounded">${req.status.toUpperCase()}</span></td>
        <td class="p-3">
          <button class="approve-btn text-green-600 mr-2" data-id="${req.id}">✔</button>
          <button class="reject-btn text-red-600" data-id="${req.id}">✖</button>
        </td>
      `;

      tbody.appendChild(tr);
    });

    // Event delegation for Approve and Reject buttons
    tbody.addEventListener('click', async (e) => {
      const id = e.target.dataset.id;
      if (!id) return;

      let newStatus = '';
      if (e.target.classList.contains('approve-btn')) {
        newStatus = 'approved';
      } else if (e.target.classList.contains('reject-btn')) {
        newStatus = 'rejected';
      }

      if (newStatus) {
        const res = await fetch(`http://127.0.0.1:8000/requests/${id}/`, {
          method: 'PATCH',
          headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ status: newStatus })
        });

        if (res.ok) {
          alert('Status updated successfully.');
          location.reload();
        } else {
          alert('Failed to update status.');
        }
      }
    });

  } catch (error) {
    alert('Error: ' + error.message);
  }
});
