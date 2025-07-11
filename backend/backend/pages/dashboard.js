document.addEventListener('DOMContentLoaded', async () => {

  const datePicker = document.getElementById("datePicker");

  if (datePicker) {
    const today = new Date().toISOString().split('T')[0];
    datePicker.value = today;

    datePicker.addEventListener("change", () => {
      const selectedDate = datePicker.value;

      // تحديث البيانات بناءً على التاريخ
      updateAttendanceForDate(subjectName, selectedDate);
    });
  }

  async function updateAttendanceForDate(subjectName, selectedDate) {
    const token = localStorage.getItem('accessToken');
    try {
      const response = await fetch('http://localhost:8000/attendance/', {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer ' + token,
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();

      const filtered = data.filter(item => 
        item.session_date?.class_session?.subject?.name === subjectName &&
        item.session_date?.session_date === selectedDate
      );

      const total = filtered.length;
      const presentCount = filtered.filter(item => item.status === 'present').length;
      const absentCount = total - presentCount;

      const presentPercentage = total ? Math.round((presentCount / total) * 100) : 0;
      const absentPercentage = total ? Math.round((absentCount / total) * 100) : 0;

      document.querySelector('.present-text-count').textContent = presentCount;
      document.querySelector('.absent-count-text').textContent = absentCount;
      document.querySelector('.present-percentage').textContent = `${presentPercentage}%`;
      document.querySelector('.absent-percentage').textContent = `${absentPercentage}%`;

      const presentCircle = document.querySelector('.present-circle');
      const absentCircle = document.querySelector('.absent-circle');
      if (presentCircle) presentCircle.setAttribute('stroke-dasharray', `${presentPercentage}, 100`);
      if (absentCircle) absentCircle.setAttribute('stroke-dasharray', `${absentPercentage}, 100`);
    } catch (error) {
      console.error('Error updating attendance for date:', error);
    }
  }

  const urlParams = new URLSearchParams(window.location.search);
  const subjectName = urlParams.get('subject');
  loadMonthlyAttendanceGraph(subjectName);
  const token = localStorage.getItem('accessToken');

  if (!token) {
    alert('No access token found. Please log in.');
    return;
  }

  if (!subjectName) {
    alert('No subject name found in URL');
    return;
  }

  try {
    const response = await fetch('http://localhost:8000/attendance/', {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      alert('Failed to fetch attendance: ' + (errorData.detail || response.statusText));
      return;
    }

    const data = await response.json();

    const filtered = data.filter(item =>
      item.session_date?.class_session?.subject?.name === subjectName
    );

    const total = filtered.length;
    const presentCount = filtered.filter(item => item.status === 'present').length;
    const absentCount = total - presentCount;


    const presentPercentage = total ? Math.round((presentCount / total) * 100) : 0;
    const absentPercentage = total ? Math.round((absentCount / total) * 100) : 0;

    // ✅ تحديث البيانات في الصفحة
    document.querySelector('.present-text-count').textContent = presentCount;
    document.querySelector('.absent-count-text').textContent = absentCount;
    document.querySelector('.present-percentage').textContent = `${presentPercentage}%`;
    document.querySelector('.absent-percentage').textContent = `${absentPercentage}%`;

    // ✅ تغيير شكل الدايرة بناءً على النسبة
    const presentCircle = document.querySelector('.present-circle');
    const absentCircle = document.querySelector('.absent-circle');

    if (presentCircle) {
      presentCircle.setAttribute('stroke-dasharray', `${presentPercentage}, 100`);
    }

    if (absentCircle) {
      absentCircle.setAttribute('stroke-dasharray', `${absentPercentage}, 100`);
    }

  } catch (error) {
    console.error('Fetch error:', error);
    alert('An error occurred while fetching attendance data.');
  }

  // 🟡 Fetch enrollments and count based on subject name
try {
  const enrollResponse = await fetch('http://localhost:8000/enrollments/', {
    method: 'GET',
    headers: {
      'Authorization': 'Bearer ' + token,
      'Content-Type': 'application/json'
    }
  });

  if (!enrollResponse.ok) {
    const errorData = await enrollResponse.json();
    alert('Failed to fetch enrollments: ' + (errorData.detail || enrollResponse.statusText));
    return;
  }

  const enrollments = await enrollResponse.json();

  // فلترة الطلاب اللي مسجلين في المادة بناءً على الاسم
  const subjectEnrollments = enrollments.filter(
    e => e.subject?.name === subjectName
  );

  // تحديث عدد الطلاب في الصفحة
  document.querySelector('.student-count').textContent = subjectEnrollments.length;

} catch (error) {
  console.error('Enrollment fetch error:', error);
  alert('An error occurred while fetching enrollments.');
}
async function loadMonthlyAttendanceGraph(subjectName) {
  const token = localStorage.getItem('accessToken');

  try {
    const response = await fetch('http://localhost:8000/attendance/', {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('❌ Error fetching attendance:', errorData);
      return;
    }

    const data = await response.json();

    const now = new Date();
    const currentMonth = now.getMonth();
    const currentYear = now.getFullYear();

    const filtered = data.filter(item => {
      const date = new Date(item.session_date?.session_date);
      return item.session_date?.class_session?.subject?.name === subjectName &&
             date.getMonth() === currentMonth &&
             date.getFullYear() === currentYear &&
             item.status === "present";
    });

    const attendancePerDay = {};
    filtered.forEach(item => {
      const day = new Date(item.session_date.session_date).getDate();
      attendancePerDay[day] = (attendancePerDay[day] || 0) + 1;
    });

    const days = Array.from({ length: 31 }, (_, i) => i + 1);
    const values = days.map(day => attendancePerDay[day] || 0);

    const canvas = document.getElementById('monthlyAttendanceChart');
    if (!canvas) {
      console.warn('monthlyAttendanceChart not found in HTML');
      return;
    }

    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: days.map(day => `Day ${day}`),
        datasets: [{
          label: `Present - ${subjectName}`,
          data: values,
          backgroundColor: 'rgba(54, 162, 235, 0.6)',
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Attendance Per Day (This Month)'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1
            }
          }
        }
      }
    });
  } catch (error) {
    console.error('❌ Fetch failed:', error);
  }
}

});
