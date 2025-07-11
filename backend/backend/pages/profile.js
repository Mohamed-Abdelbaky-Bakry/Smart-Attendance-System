document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("accessToken");
  const params = new URLSearchParams(window.location.search);
  const studentName = decodeURIComponent(params.get("name"));

  if (!token || !studentName) {
    alert("Missing token or student name.");
    return;
  }

  try {
    const allRequests = await fetch("http://127.0.0.1:8000/requests/", {
      headers: { Authorization: "Bearer " + token }
    }).then(res => res.json());

    const studentRequests = allRequests.filter(
         r => r.student.account.name.trim().toLowerCase() === studentName.trim().toLowerCase()
    );
    const requestsCount = studentRequests.length;

    // 1. Get student list
    const students = await fetch("http://localhost:8000/students/", {
      headers: { Authorization: "Bearer " + token }
    }).then(res => res.json());

    // 2. Match name exactly
    const student = students.find(
      s => s.account.name.trim().toLowerCase() === studentName.trim().toLowerCase()
    );

    if (!student) {
      alert(`Student '${studentName}' not found.`);
      return;
    }

    // 3. Get attendance records
    const attendance = await fetch("http://localhost:8000/attendance/", {
      headers: { Authorization: "Bearer " + token }
    }).then(res => res.json());

    const studentAttendance = attendance.filter(
  a => a.student.account.name.trim().toLowerCase() === studentName.trim().toLowerCase()
);


    const presentCount = studentAttendance.filter(
  a => a.status && a.status.toLowerCase() === "present"
).length;

const totalSessions = studentAttendance.length;


    const percentage = totalSessions > 0
      ? Math.round((presentCount / totalSessions) * 100)
      : 0;

    // 4. Update DOM
    document.querySelector(".text-2xl.font-bold.text-gray-700").textContent = student.account.name;

    document.querySelector("div.bg-gray-800 p.text-2xl").textContent = requestsCount;

    // Update department
    const departmentName = student.department?.name || "Communication";
    document.querySelectorAll("p.text-gray-500")[0].textContent = departmentName;

    // Update grade
    const gradeMap = {
      "1": "First year",
      "2": "Second year",
      "3": "Third year",
      "4": "Fourth year"
    };
    const gradeText = gradeMap[student.grade] || "N/A";
    document.querySelectorAll("p.text-gray-500")[1].textContent = gradeText;

    // Attendance summary
    const presentText = `Present ${presentCount}/${totalSessions}`;
    document.querySelector("div.bg-teal-700 p.text-2xl").textContent = `Present ${presentCount}/${totalSessions}`;

    // Percentage in performance circle
    const circle = document.querySelector("svg circle[stroke='green']");
    const percentText = document.querySelector(".text-green-500");
    
    const percent = totalSessions > 0 ? Math.round((presentCount / totalSessions) * 100) : 0;
document.querySelector(".text-green-500").textContent = `${percent}%`;
document.querySelector("svg circle[stroke='green']").setAttribute("stroke-dashoffset", 282.6 - (percent / 100) * 282.6);


    circle.setAttribute("stroke-dashoffset", 282.6 - (percentage / 100) * 282.6);
    percentText.textContent = `${percentage}%`;

    // Student details in yellow box
    const yellowBox = document.querySelector(".bg-yellow-100");
    const infoParagraphs = yellowBox.querySelectorAll("p");

    infoParagraphs[0].innerHTML = `<strong>Student ID:</strong> ${student.student_code}`;
    infoParagraphs[1].innerHTML = `<strong>E-mail:</strong> ${student.account.email}`;
    infoParagraphs[2].innerHTML = `<strong>Grade:</strong> ${student.grade}`;
    infoParagraphs[3].innerHTML = `<strong>Mobile Number:</strong> ${student.account.mobile_number || "N/A"}`;

  } catch (error) {
    console.error(error);
    alert("Error fetching profile data.");
  }
});
