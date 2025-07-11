    document.addEventListener('DOMContentLoaded', async () => {
  const token = localStorage.getItem('accessToken');
  const tableBody = document.querySelector('table tbody');

  if (!token) {
    alert("Please log in first.");
    return;
  }

  const instructorAccountId = 2; // Replace with dynamic logic if needed

  try {
    // Get all teaches
    const teaches = await fetch('http://localhost:8000/teaches/', {
      headers: { 'Authorization': 'Bearer ' + token }
    }).then(r => r.ok ? r.json() : Promise.reject('teaches fetch failed'));

    // Get subject IDs taught by this instructor
    const mySubjectIds = teaches
      .filter(t => t.instructor.account === instructorAccountId)
      .map(t => t.subject.id);

    if (mySubjectIds.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="6" class="p-2">You aren’t teaching any subjects yet.</td></tr>';
      return;
    }

    // Fetch all enrollments
    const enrollments = await fetch('http://localhost:8000/enrollments/', {
      headers: { 'Authorization': 'Bearer ' + token }
    }).then(r => r.ok ? r.json() : Promise.reject('enrollments fetch failed'));

    // Filter enrollments for this instructor's subjects
    const myEnrolls = enrollments.filter(e => mySubjectIds.includes(e.subject.id));

    // Fetch all students
    const students = await fetch('http://localhost:8000/students/', {
      headers: { 'Authorization': 'Bearer ' + token }
    }).then(r => r.ok ? r.json() : Promise.reject('students fetch failed'));

    // Create lookup dictionary for students
    const studentMap = {};
    students.forEach(s => {
      studentMap[s.account.id] = {
        name: s.account.name,
        email: s.account.email,
        id: s.account.id,
      };
    });

    // Render table rows
    tableBody.innerHTML = '';
    myEnrolls.forEach(e => {
      const subject = e.subject;
      const student = studentMap[e.student.account];

      if (!student) return;

      const row = `
        <tr>
          <td class="border p-2">${student.id}</td>
          <td class="border p-2">${student.name}</td>
          <td class="border p-2">${student.email}</td>
          <td class="border p-2">${e.student.grade}</td>
          <td class="border p-2">${subject.code}</td>
          <td class="border p-2">${subject.name}</td>
          <td class="border p-2">
      <a href="http://127.0.0.1:5500/pages/Profile.html?name=${encodeURIComponent(student.name)}"
         class="text-white bg-blue-500 px-3 py-1 rounded hover:bg-blue-600">
        Check Profile
      </a>
    </td>
        </tr>
      `;
      tableBody.innerHTML += row;
    });

    if (myEnrolls.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="6" class="p-2">No students enrolled in your subjects.</td></tr>';
    }

  } catch (err) {
    console.error(err);
    alert('Error loading data; see console for details.');
  }
});
